import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import CTransformers
from langchain.llms import Replicate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv
import tempfile

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Preguntame lo que quieras sobre los documentos 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]

# def conversation_chat(query, chain, history):
#     result = chain({"question": query, "chat_history": history})
#     history.append((query, result["answer"]))
#     return result["answer"]

def display_chat_history(vector_store):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Pegunta:", placeholder="Pregunta sobre los documentos", key='input')
            submit_button = st.form_submit_button(label='Enviar') #Send

        if submit_button and user_input:
            with st.spinner('Generando respuesta...'):
                output = retrieve_bot_answer(user_input, vector_store)#, chain, st.session_state['history'])
            
            st.session_state['history'].append(output)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

# def create_conversational_chain(vector_store):
#     load_dotenv()
#     #Create llm
#     # llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
#     #                     streaming=True, 
#     #                     callbacks=[StreamingStdOutCallbackHandler()],
#     #                     model_type="llama", config={'max_new_tokens': 500, 'temperature': 0.01})
#     llm = Replicate(
#         streaming = True,
#         model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
#         callbacks=[StreamingStdOutCallbackHandler()],
#         input = {"temperature": 0.01, "max_length" :500,"top_p":1}) #0.01
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    
#     chain = RetrievalQA.from_chain_type(llm=llm, 
#                                 chain_type='stuff',
#                                 retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
#                                 #memory=memory,
#                                 chain_type_kwargs=chain_type_kwargs)
#     return chain

####
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in Spanish:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return prompt

def load_model():
    """
    Load a locally downloaded model.

    Parameters:
        model_path (str): The path to the model to be loaded.
        model_type (str): The type of the model.
        max_new_tokens (int): The maximum number of new tokens for the model.
        temperature (float): The temperature parameter for the model.

    Returns:
        CTransformers: The loaded model.

    Raises:
        FileNotFoundError: If the model file does not exist.
        SomeOtherException: If the model file is corrupt.
    """
    load_dotenv()
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1})

    return llm

# def create_chunk(uploaded_files):
#     if uploaded_files:
#         text = []
#         for file in uploaded_files:
#             file_extension = os.path.splitext(file.name)[1]
#             with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#                 temp_file.write(file.read())
#                 temp_file_path = temp_file.name

#             loader = None
#             if file_extension == ".pdf":
#                 loader = PyPDFLoader(temp_file_path)
#             elif file_extension == ".docx" or file_extension == ".doc":
#                 loader = Docx2txtLoader(temp_file_path)
#             elif file_extension == ".txt":
#                 loader = TextLoader(temp_file_path)

#             if loader:
#                 text.extend(loader.load())
#                 os.remove(temp_file_path)

#         text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
#         text_chunks = text_splitter.split_documents(text)
#         return text_chunks

def create_retrieval_qa_chain(vector_store):
    """
    Creates a Retrieval Question-Answering (QA) chain using a given language model, prompt, and database.

    This function initializes a RetrievalQA object with a specific chain type and configurations,
    and returns this QA chain. The retriever is set up to return the top 3 results (k=3).

    Args:
        llm (any): The language model to be used in the RetrievalQA.
        prompt (str): The prompt to be used in the chain type.
        db (any): The database to be used as the retriever.

    Returns:
        RetrievalQA: The initialized QA chain.
    """
    qa_prompt = (
        set_custom_prompt()
    )
    
    chain_type_kwargs = {"prompt": qa_prompt}
    
    llm = load_model()
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type='stuff',
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        #memory=memory,
        chain_type_kwargs=chain_type_kwargs,
    )
    return qa_chain


# def create_retrieval_qa_bot(vector_store
#     # model_name="sentence-transformers/all-MiniLM-L6-v2",
#     # #persist_dir="./db",
#     # device="cpu",
# ):
#     """
#     This function creates a retrieval-based question-answering bot.

#     Parameters:
#         model_name (str): The name of the model to be used for embeddings.
#         persist_dir (str): The directory to persist the database.
#         device (str): The device to run the model on (e.g., 'cpu', 'cuda').

#     Returns:
#         RetrievalQA: The retrieval-based question-answering bot.

#     Raises:
#         FileNotFoundError: If the persist directory does not exist.
#         SomeOtherException: If there is an issue with loading the embeddings or the model.
#     """

#     # embeddings = HuggingFaceEmbeddings(
#     #     model_name=model_name,
#     #     model_kwargs={"device": device},
#     # )
   
#     #db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

#     qa_prompt = (
#         set_custom_prompt()
#     )  # Assuming this function exists and works as expected

#     llm = load_model()
    
#     # vector_store = FAISS.from_documents(create_chunk(), embedding=embeddings)
    
#     qa = create_retrieval_qa_chain(
#         llm=llm, prompt=qa_prompt, db=vector_store
#     )  # Assuming this function exists and works as expected
    

#     return qa

def retrieve_bot_answer(query, vector_store):
    """
    Retrieves the answer to a given query using a QA bot.

    This function creates an instance of a QA bot, passes the query to it,
    and returns the bot's response.

    Args:
        query (str): The question to be answered by the QA bot.

    Returns:
        dict: The QA bot's response, typically a dictionary with response details.
    """
    qa_bot_instance = create_retrieval_qa_chain(vector_store) # esta es la query
    bot_response = qa_bot_instance({"query": query})
    return bot_response