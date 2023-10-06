# LLM2-db-documental

# Streamlit Chat con Langchain 

Este es un proyecto que utiliza Streamlit y Langchain para crear un chat basado en modelos de lenguaje de Hugging Face. Con esta aplicación, se puede interactuar con un modelo de lenguaje que obtiene la información de los documentos cargados por el usuario y responde a las preguntas basado en dicha información

## Requisitos

El primer paso es acceder al directorio de trabajo y crear el entorno virtual. Luego acceder al mismo

```bash
cd ruta/al/directorio
python -m venv st_venv
.\st_venv\Scripts\activate

```

Una vez en el entorno virtual se deben instalar las bibliotecas del archivo requirements.txt:

```bash
langchain
torch
accelerate
sentence_transformers
streamlit_chat
streamlit
faiss-cpu
tiktoken
ctransformers
huggingface-hub
pypdf
python-dotenv
replicate
docx2txt
```

## Uso

Se ejecuta la aplicación en streamlit con el siguiente comando:
```bash
streamlit run app.py
```

## Código

El archivo app.py, importa las siguientes librerías:
```bash
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
import os
import tempfile
import utils as utils
import importlib
importlib.reload(utils)
```

Se define una función llamada main() que será el punto de entrada principal de la aplicación de chatbot en Streamlit.
```bash
def main():
```

Se llama a la función initializeSessionState() del módulo utils para inicializar el estado de la sesión de la aplicación.
```bash
utils.initializeSessionState()
```

Esta función se encarga de configurar el estado de la sesión. Verifica si ciertas claves ('history', 'generated', 'past') están presentes en el estado de la sesión.
Si no están presentes, las inicializa con valores predeterminados.
```bash
def initializeSessionState():

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Preguntame lo que quieras sobre los documentos 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]
```

Se establece el título principal de la aplicación y se crea una barra lateral en la interfaz de usuario donde los usuarios pueden cargar mútliples documentos.
```bash
st.title("ChatBot de documentos usando llama2 :books:")
st.sidebar.title("Procesamiento de documentos")
    uploadedFiles = st.sidebar.file_uploader("Suba aquí los documentos", accept_multiple_files=True)
```

Si se han cargado archivos, se inicializa una lista vacía llamada 'text'.
```bash
    if uploadedFiles:
        text = []
```

Se recorren uno a uno los archivos cargados y se obtiene la extensión del nombre de cada uno.
```bash
        for file in uploadedFiles:
            fileExtension = os.path.splitext(file.name)[1]
```
Se utiliza la biblioteca tempfile.NamedTemporaryFile() para almacenar temporalmente datos en disco. El parámetro delete=False asegura que el archivo temporal no se elimine automáticamente cuando se cierre.
El contenido del archivo cargado (file) se escribe en el archivo temporal (tempFile) utilizando el método write().
Luego se obtiene la ruta del archivo temporal recién creado y se almacena en la variable tempFilePath
```bash
            with tempfile.NamedTemporaryFile(delete=False) as tempFile:
                tempFile.write(file.read())
                tempFilePath = tempFile.name
```

Se crea la variable loader que contendrá un objeto de la clase PyPDFLoader, Docx2txtLoader o TextLoader dependiendo la extensión del archivo 'file'.
El objeto generado será un documento que tendrá: el contenido del archivo como una cadena de texto y la metadata 
```bash
            loader = None
            if fileExtension == ".pdf":
                loader = PyPDFLoader(tempFilePath)
            elif fileExtension == ".docx" or fileExtension == ".doc":
                loader = Docx2txtLoader(tempFilePath)
            elif fileExtension == ".txt":
                loader = TextLoader(tempFilePath)
```
Si loader contiene un objeto, se carga el contenido de ese objeto (texto y metadatos) a la variable text y se borra el archivo temporal. De este modo la variable text contendrá una lista de documentos con su texto y su metadata (etiquetas, nombres de archivo). El bucle 'for' vuelve a recorrer uploadedFiles hasta realizar el proceso con todos los archivos cargados.
 ```bash
            if loader:
                text.extend(loader.load())
                os.remove(tempFilePath)
```


Se instancia un objeto de la clase CharacterTextSplitter, con los siguientes argumentos:
* separator: En este caso, estamos usando "\n" como separador, lo que significa que cada fragmento será separado por dos saltos de línea consecutivos.
* chunk_size: el tamaño máximo deseado para cada fragmento. En este caso, se establece el tamaño máximo en 1000 caracteres.
* chunk_overlap: el número de caracteres que se solapan entre dos fragmentos adyacentes. En este caso, se establece el overlap en 100 caracteres.
* length_function: la función que se utilizará para medir la longitud de cada fragmento. En este caso, se utiliza la función integrada len() para contar el número de caracteres en cada fragmento.

Luego split_documents() recibe la cadena de texto original y la divide en fragmentos según los parámetros especificados en la instancia de CharacterTextSplitter. El resultado es una lista de fragmentos de texto, donde cada fragmento tiene un tamaño menor o igual al valor especificado en chunk_size. Si un fragmento supera el tamaño máximo, se dividen en varios fragmentos menores y se agregan a la lista resultante.
 ```bash
        textSplitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        textChunks = textSplitter.split_documents(text)
```

Se carga el modelo capaz de generar representaciones numéricas de texto, llamadas "embeddings", y se establece que debe ser ejecutado en una tarjeta gráfica (device='cuda') para realizar las operaciones matemáticas necesarias

 ```bash
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                           model_kwargs={'device': 'cuda'})
```

Se utiliza la clase FAISS de la biblioteca langchain.vectorstores.faiss para crear un objeto VectorStore. La función from_documents() toma dos argumentos: una lista de objetos Document y un objeto Embeddings. En este caso, se están pasando los siguientes valores como argumentos:
textChunks: Es una lista de cadenas de caracteres que representan las diferentes partes del texto que se desea indexar. Cada cadena corresponde a un fragmento del texto original.
embeddings: Es un objeto Embeddings que contiene información sobre cómo codificar el texto en vectores numéricos
 ```bash
        vectorStore = FAISS.from_documents(textChunks, embedding=embeddings)
```

Se pasa el objeto vectorStore a la función createConversationalChain, y se asigna a la variable 'chain'
```bash
        chain = utils.createConversationalChain(vectorStore)```
```
La función createConversationalChain crea una cadena de conversaciones para generar respuestas basadas en el contexto del chat. Utiliza un modelo de lenguaje (LLM) para generar texto y un recuperador para responder según el contexto. Además, utiliza una memoria para almacenar las conversaciones previas y ayudar a mejorar la comprensión del contexto.

La función comienza inicializando una cadena de conversaciones llamando a la clase ConversationalRetrievalChain. Esta clase es parte de la biblioteca de Python transformers, utilizada para implementar modelos de lenguaje y procesamiento de lenguaje natural.

Luego, la función configura los parámetros específicos para la generación de texto, la búsqueda y la gestión de memoria. Estos parámetros incluyen la temperatura del modelo de lenguaje, el tipo de cadena de conversaciones, el número máximo de nuevas tokens permitidas, si se debe realizar muestreo, el número de secuencias de regresión deseadas y el identificador del token de fin de oración.

Finalmente, la función devuelve la cadena de conversaciones configurada.
```bash
def createConversationalChain(vectorStore):
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
    llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0.01})
   
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vectorStore.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain
```

Por último, se llama a la función displayChatHistory, pasándole de argumento la cadena de conversaciones generada anteriormente
```bash
        utils.displayChatHistory(chain)
```

La función displayChatHistory muestra una interfaz de chat para interactuar con una cadena de conversación y ver el historial de chat, el cual incluye las consultas de los usuarios y las respuestas del sistema en un formato de conversación.
Argumentos:
chain (callable): Una función u objeto callable que toma un diccionario con una pregunta
y chat_history como entrada, y devuelve un diccionario con una respuesta.
```bash
def displayChatHistory(chain):
    replyContainer = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            userInput = st.text_input("Pegunta:", placeholder="Pregunta sobre los documentos", key='input')
            submitButton = st.form_submit_button(label='Enviar')

        if submitButton and userInput:
            with st.spinner('Generando respuesta...'):
                output = conversationChat(userInput, chain, st.session_state['history'])

            st.session_state['past'].append(userInput)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with replyContainer:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")
```
La función displayChatHistory utiliza por dentro a la función conversationChat, la cual tiene varios componentes importantes:

result = chain({"question": query, "chat_history": history}): Aquí se llama a la función chain con un diccionario que contiene la pregunta actual (query) y el historial de conversación anterior (history). La función chain devuelve un resultado que incluye la respuesta a la pregunta actual.

history.append((query, result["answer"])): Se agrega la pregunta actual y su respuesta correspondiente al final del historial de conversación.

return result["answer"]: Finalmente, se devuelve solo la respuesta a la pregunta actual.

En otras palabras, esta función simplemente envía una pregunta a la función chain y obtiene una respuesta. Luego, agrega la pregunta y la respuesta al historial de conversación y devuelve la respuesta.
```bash
def conversationChat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]
```



***
***
## Google Colab

🚧 En construcción 🚧

(Próximamente las instrucciones para ejecutar el modelo de chatbot desde Google Colab)


## Colaboradores

- Carla Celina Pezzone
- David Echajaya
- Jeremías Pombo
- Jerson Carbajal Ramirez
- René Sebastián Joo Cisneros