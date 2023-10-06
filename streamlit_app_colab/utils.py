import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
# from langchain.llms import CTransformers
# from langchain.llms import Replicate
from langchain.memory import ConversationBufferMemory
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain import HuggingFacePipeline
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

#model_id = "codellama/CodeLlama-34b-Instruct-hf"
#model_id = "meta-llama/Llama-2-13b-chat-hf"
model_id = "meta-llama/Llama-2-7b-chat-hf"
#model_id = "model/models--meta-llama--Llama-2-7b-chat-hf"

# Loads the appropriate tokenizer for the specified model checkpoint
tokenizer = AutoTokenizer.from_pretrained(model_id,
                                          use_auth_token=True,)
# Initializes a language model
model = AutoModelForCausalLM.from_pretrained(model_id,
                                            device_map='auto',
                                             torch_dtype='auto',#torch.float32,
                                             use_auth_token=True,
                                             local_files_only=False,
                                            #cache_dir="model/"
                                            )

def initialize_session_state():
    '''
    Initializes the session state for a Streamlit application.

    This function checks if certain keys ('history', 'generated', 'past') are present in the session state.
    If they are not present, it initializes them with default values.

    Returns:
        None
    '''
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Preguntame lo que quieras sobre los documentos 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]

def conversation_chat(query, chain, history):
    '''
    Conducts a conversation by processing a user query using a conversation chain.

    Args:
        query (str): The user's input query.
        chain (callable): A function or callable object that takes a dictionary with a question
            and chat_history as input and returns a dictionary with an answer.
        history (list): A list of conversation history tuples, where each tuple contains the user's query
            and the system's response.

    Returns:
        str: The answer generated by the conversation chain for the user's query.

    The function processes the user's query by passing it to the provided conversation chain along with the
    conversation history. The resulting answer is then appended to the history list for reference.
    '''
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    '''
    Displays a chat interface to interact with a conversation chain and view chat history.

    Args:
        chain (callable): A function or callable object that takes a dictionary with a question
            and chat_history as input and returns a dictionary with an answer.

    The function creates a chat interface where users can input questions and receive responses using
    the provided conversation chain. It also displays the chat history, including user queries and
    system responses, in a conversation format.
    '''
    replyContainer = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            userInput = st.text_input("Pegunta:", placeholder="Pregunta sobre los documentos", key='input')
            submitButton = st.form_submit_button(label='Send')

        if submitButton and userInput:
            with st.spinner('Generando respuesta...'):
                output = conversation_chat(userInput, chain, st.session_state['history'])

            st.session_state['past'].append(userInput)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with replyContainer:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

def create_conversational_chain(vector_store):
    '''
    Creates a conversational chain for generating responses in a chat-based application.

    Args:
        vectorStore: A vector store from data structure used for retrieval-based chat models.

    Returns:
        ConversationalRetrievalChain: A conversational chain that combines a language model (LLM)
        for text generation with a retriever for context-based responses.

    This function initializes a conversational chain, which combines a language model (LLM) for text generation
    with a retriever for context-based responses. The chain is configured with specific parameters for text generation,
    retrieval, and memory management.
    '''
    #Create llm
    pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                max_new_tokens = 512,
                do_sample=True,
                top_k=30,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id
                )
    llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0.2})
    #llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
     #                   streaming=True, 
     #                   callbacks=[StreamingStdOutCallbackHandler()],
      #                  model_type="llama", config={'max_new_tokens': 500, 'temperature': 0.01, 'gpu_layers': 24})
    #llm = Replicate(
    #     streaming = True,
    #     model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
    #     callbacks=[StreamingStdOutCallbackHandler()],
    #     input = {"temperature": 0.01, "max_length" :500,"top_p":1}) #0.01
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain