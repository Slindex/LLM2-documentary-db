import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import CTransformers
from langchain.llms import Replicate
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
# from langchain.document_loaders import PyPDFLoader
# from langchain.document_loaders import TextLoader
# from langchain.document_loaders import Docx2txtLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# import os
from dotenv import load_dotenv
# import tempfile


def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Preguntame lo que quieras sobre los documentos 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Pegunta:", placeholder="Pregunta sobre los documentos", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generando respuesta...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

def create_conversational_chain(vector_store):
    load_dotenv()
    #Create llm
    # llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
    #                     streaming=True, 
    #                     callbacks=[StreamingStdOutCallbackHandler()],
    #                     model_type="llama", config={'max_new_tokens': 500, 'temperature': 0.01})
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1}) #0.01
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain