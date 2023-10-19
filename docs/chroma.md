<center>

# Alternativa de Base de Datos Vectorial Open Source 
</center> 

<p align=center>
<img src="src\chroma.png" height=50 weight=50>
<p>

## Definición - Chroma

Es una base de datos vectorial de código abierto, flexible y sencilla, capaz de guardar vectores (generalmente embeddings) para su uso posterior en LLMs (grandes modelos de lenguaje) y también sirve como base para motores de búsqueda semánticos que operan con datos textuales. Chroma ofrece la gestión de grandes volúmenes de datos no estructurados y semiestructurados.

## Instalación
Para instalar la biblioteca ChromDB más actualizada se tiene que ejecutar el siguiente comando: 

```bash
pip install chromadb -U
```

Si está trabajando desde una computadora portátil Jupyter, utilice el comando

```bash
!pip install chromadb -U
```

El indicador "-U" se utiliza para actualizar ChromDB si tiene instalada una versión anterior. Se recomienda utilizar la versión 3.10 de Python o una versión posterior.

## Características

Se integra con LangChain y Chainlit, es un framework que utiliza LLMs para crear aplicaciones de inteligencia artificial, tales como chatbots similares al famoso ChatGPT.

<p align=center>
<img src="src\langchain.png" height=130 weight=130>
<p>
<br/>

## ChatLlama2 para Documentos usando Chainlit

Esta solución está comprendida por 2 etapas la primera es la Ingestión de los documentos en la Base de Datos Vectorial Chroma y la segunda es la consulta de documentos.

### Ingestión de Documentos 

```python
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings import SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma 
import os 

from langchain.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db")


def create_vector_database():
    
    """
    Creates a vector database using document loaders and embeddings.
    This function loads data from PDF, markdown and text files in the 'data/' directory,
    splits the loaded documents into chunks, transforms them into embeddings,
    and finally persists the embeddings into a Chroma vector database.

    """
    
    # Initialize loaders for different file types
    pdf_loader = DirectoryLoader("data/", glob="**/*.pdf", loader_cls=PyPDFLoader)
    markdown_loader = DirectoryLoader(
        "data/", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
    )
    text_loader = DirectoryLoader("data/", glob="**/*.txt", loader_cls=TextLoader)

    all_loaders = [pdf_loader, markdown_loader, text_loader]

    # Load documents from all loaders
    documents = []
    for loader in all_loaders:
        documents.extend(loader.load())
    
    # Split loaded documents into chunks
    print("splitting into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100, length_function=len)
    chunked_documents = text_splitter.split_documents(documents)
    
    #Create embeddings here
    print("Loading sentence transformers model")
    embeddings = SentenceTransformerEmbeddings(
                                model_name="./model/all-MiniLM-L6-v2",
                                model_kwargs={"device": "cpu"})
    
    # Create and persist a Chroma vector database from the chunked documents
    print(f"Creating embeddings. May take some minutes...")
    vector_database = Chroma.from_documents(
                                documents=chunked_documents, 
                                embedding=embeddings, 
                                persist_directory=DB_DIR)
    vector_database.persist()
    vector_database=None 

    print(f"Ingestion complete! You can now run to query your documents")

if __name__ == "__main__":
    create_vector_database()
```

### Librería Utils
Esta librería contiene funciones que servirán para crear la aplicación

```python
from langchain.memory import ConversationBufferMemory
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings 
import os

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db")

prompt_template = """
Eres un lector experto de documentos desde hace muchos años. Si no sabes la respuesta, simplemente menciona que no la sabes, no intentes inventar una respuesta.
SIEMPRE devuelve todas tus respuestas en Español, es necesario traducir sus respuestas al Español sobre los documentos.
El ejemplo de su respuesta debería ser:

Contexto: {context}
Pregunta: {question}

"""
def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return prompt

def create_retrieval_qa_bot(
    model_name="./model/all-MiniLM-L6-v2",
    persist_dir=DB_DIR,
    device="cpu",
):
    """
    This function creates a retrieval-based question-answering bot.

    Parameters:
        model_name (str): The name of the model to be used for embeddings.
        persist_dir (str): The directory to persist the database.
        device (str): The device to run the model on (e.g., 'cpu', 'cuda').

    Returns:
        RetrievalQA: The retrieval-based question-answering bot.

    Raises:
        FileNotFoundError: If the persist directory does not exist.
        SomeOtherException: If there is an issue with loading the embeddings or the model.
    """

    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"No directory found at {persist_dir}")

    try:
        embedding_function = SentenceTransformerEmbeddings(
            model_name=model_name, 
            model_kwargs={'device':device})
        
    except Exception as e:
        raise Exception(
            f"Failed to load embeddings with model name {model_name}: {str(e)}"
        )

    vectorStore =  Chroma(persist_directory=persist_dir, embedding_function=embedding_function)

    qa_prompt = (
        set_custom_prompt()
    )  

    try:
        qa_chain = createConversationalChain(vectorStore, qa_prompt)
 
    except Exception as e:
        raise Exception(f"Failed to create retrieval QA chain: {str(e)}")

    return qa_chain


def createConversationalChain(vectorStore,prompt):
    '''
    Creates a conversational chain for generating responses in a chat-based application.

    Args:
        vectorStore: A vector store from data structure used for retrieval-based chat models.

    Returns:
        ConversationBufferMemory: A conversational chain that combines a language model (LLM)
        for text generation with a retriever for context-based responses.

    This function initializes a conversational chain, which combines a language model (LLM) for text generation
    with a retriever for context-based responses. The chain is configured with specific parameters for text generation,
    retrieval, and memory management.
    '''
  
    llm = CTransformers(model="./model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                        streaming=True, 
                        callbacks=[StreamingStdOutCallbackHandler()],
                        model_type="llama", config={'temperature': 0.05} ,n_ctx=1024,max_tokens= 0)
   
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    
    chain = RetrievalQA.from_chain_type(llm=llm, 
                                        chain_type='stuff',
                                        retriever=vectorStore.as_retriever(search_kwargs={"k": 2}),
                                        memory=memory, 
                                        chain_type_kwargs={"prompt": prompt})
    return chain

```
### Archivo de Aplicación app.py
Éste archivo albergará todo el código que se usará para crear la aplicación de ChatBot con Chainlit

```python
import chainlit as cl
import chromadb as ch
from chromadb.config import Settings
client = ch.Client(Settings(anonymized_telemetry=False))
import utils as utils
import importlib
importlib.reload(utils)


@cl.on_chat_start
async def initialize_bot():
    """
    Initializes the bot when a new chat starts.

    This asynchronous function creates a new instance of the retrieval QA bot,
    sends a welcome message, and stores the bot instance in the user's session.
    """
    qa_chain = utils.create_retrieval_qa_bot()
    welcome_message = cl.Message(content="Starting the bot...")
    await welcome_message.send()
    welcome_message.content = (
        "Hola, Bienvenido al Chat con Documentos usando Llama2 y LangChain."
    )
    await welcome_message.update()

    cl.user_session.set("chain", qa_chain)


@cl.on_message
async def process_chat_message(message):
    """
    Processes incoming chat messages.

    This asynchronous function retrieves the QA bot instance from the user's session,
    sets up a callback handler for the bot's response, and executes the bot's
    call method with the given message and callback. The bot's answer and source
    documents are then extracted from the response.
    """
    qa_chain = cl.user_session.get("chain")
    callback_handler = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    callback_handler.answer_reached = True
    response = await qa_chain.acall(message, callbacks=[callback_handler])
    bot_answer = response["result"]

    cl.Message(bot_answer).send()
#chainlit run app.py -w
```

## Enlaces de Referencia

- [An Overview of ChromaDB: The Vector Database](https://medium.com/@kbdhunga/an-overview-of-chromadb-the-vector-database-206437541bdd)
- [Tutorial de la base de datos vectorial Chroma](https://anderfernandez.com/blog/chroma-vector-database-tutorial/)