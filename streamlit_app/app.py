import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
import os
#from dotenv import load_dotenv
import tempfile
import utils as utils

import importlib
importlib.reload(utils)

def main():
    '''
    Main function for the Streamlit-based ChatBot application.

    This function sets up and runs the ChatBot application, which allows users to upload and process
    multiple documents, create embeddings, and interact with a conversational ChatBot.

    Returns:
        None
    '''
    #load_dotenv()
    # Initialize session state
    utils.initializeSessionState()
    
    st.title("ChatBot de documentos usando llama2 :books:")
    
    # Initialize Streamlit sidebar where uploaded files
    st.sidebar.title("Procesamiento de documentos")
    uploadedFiles = st.sidebar.file_uploader("Suba aquí los documentos", accept_multiple_files=True)

    if uploadedFiles:
        text = []
        for file in uploadedFiles:
            fileExtension = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False) as tempFile:
                tempFile.write(file.read())
                tempFilePath = tempFile.name

            loader = None
            if fileExtension == ".pdf":
                loader = PyPDFLoader(tempFilePath)
            elif fileExtension == ".docx" or fileExtension == ".doc":
                loader = Docx2txtLoader(tempFilePath)
            elif fileExtension == ".txt":
                loader = TextLoader(tempFilePath)

            if loader:
                text.extend(loader.load())
                os.remove(tempFilePath)

        textSplitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        textChunks = textSplitter.split_documents(text)

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                           model_kwargs={'device': 'cuda'})

        # Create vector store
        vectorStore = FAISS.from_documents(textChunks, embedding=embeddings)

        # Create the chain object
        chain = utils.createConversationalChain(vectorStore)

        utils.displayChatHistory(chain)

if __name__ == "__main__":
    main()