# LLM2-db-documental

# Streamlit Chat con Langchain 

Este es un proyecto que utiliza Streamlit y Langchain para crear un chat basado en modelos de lenguaje de Hugging Face. Con esta aplicación, se puede interactuar con un modelo de lenguaje que obtiene la información de los documentos cargados por el usuario y responde a las preguntas basado en dicha información.

## Requisitos

En primer lugar se debe clonar este repositorio.

```bash
git clone https://github.com/GoUpCloud/LLM2-db-documental.git
```
Luego, se debe acceder al directorio de trabajo, crear un entorno virtual de trabajo y finalmente acceder al mismo.

```bash
cd ruta/al/directorio
python -m venv st_venv
.\st_venv\Scripts\activate
```

Una vez dentro del entorno virtual se deben instalar las dependencias del proyecto que se encuentran en el archivo `requirements.txt`:

```bash
pip install -r requitements.txt
```

## Ejecución de la aplicación

Para ejecutar la aplicación en Streamlit se realiza la siguiente acción en la consola:

```bash
streamlit run app.py
```

## Tecnologías utilizadas

Se utilizan las siguientes tecnologías para esta aplicación:

* **Streamlit**: es una biblioteca de Python que facilita la creación de aplicaciones web interactivas para visualizar y compartir datos y análisis de manera sencilla, utilizando solo código Python. Permite a los desarrolladores crear interfaces de usuario de manera rápida y eficiente.
* **Langchain**: es un framework diseñado para simplificar la creación de aplicaciones utilizando grandes modelos de lenguaje. En particular se usan las siguientes funciones:
* **Transformers**: es una herramienta de código abierto desarrollada por Hugging Face que se utiliza principalmente para trabajar con modelos de procesamiento de lenguaje natural (NLP), incluyendo modelos de lenguaje preentrenados, tareas de traducción, generación de texto, análisis de sentimientos y mucho más.
* **torch**: es el framework de trabajo PyTorch, que en este caso se utiliza para el manejo de los recursos en GPU. 

## Flujo de ejecución

Se utilizan dos archivos con las funciones necesarias para la ejecución de la aplicación. Por un lado `app.py` que contiene la clase *main* y `utils.py` que contiene funcionalidades específicas.

Cuando se realiza la acción de correr la aplicación, se abre un nuevo navegador con la aplicación. Lo primero que se ejecuta es una función llamada `main()`.

```bash
def main():
```
En la primera ejecución, lo primero que realiza es la descarga del modelo y se instancia el mismo, así también el tokenizer. `AutoTokenizer` es responsable de procesar el texto a un formato que sea entendible para el modelo. `AutoModelForCausalLM` descarga el modelo y lo instancia en la variable 'model'.

````bash
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf",
                                          use_auth_token=True,)

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf",
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             use_auth_token=True,
                                             local_files_only=False)
````

A continuación, se llama a la función initializeSessionState() del módulo utils para inicializar el estado de la sesión de la aplicación.

```bash
utils.initializeSessionState()
```

Esta función se encarga de configurar el estado de la sesión. Verifica los estados de 'history', 'generated', 'past' para mantener el flujo de ejecución de las funciones de Streamlit acorde a lo programado.

En esta inicialización, en la primera ejecución, muestra un historial vacío, la primer pregunta del usuario y respuesta del chat, a modo de ejemplos de vista para mejorar la experiencia del usuario. Esto se ve en el siguiente código, el cuál se encuentra en `utils.py`.

```bash
def initializeSessionState():

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Preguntame lo que quieras sobre los documentos 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]
```

Continuando con la función `main`, se define el título principal de la aplicación y se crea una barra lateral para que los usuarios pueden cargar mútliples documentos.

```bash
st.title("ChatBot de documentos usando llama2 :books:")
st.sidebar.title("Procesamiento de documentos")
    uploadedFiles = st.sidebar.file_uploader("Suba aquí los documentos", accept_multiple_files=True)
```
Una vez que el usuario carga los documentos, se observa una barra de progreso hasta que el documento queda cargado y se inicializa una lista vacía llamada 'text'.

```bash
    if uploadedFiles:
        text = []
```

Luego, un bucle for recorren cada uno de los archivos cargados para identificar la extensión de cada archivo. Esto se hace para poder leer distintos formatos de archivos.

```bash
        for file in uploadedFiles:
            fileExtension = os.path.splitext(file.name)[1]
```

Se utiliza la librería `tempfile` y en particular la función `NamedTemporaryFile()` para almacenar temporalmente los datos en disco como `tempFile`. El parámetro `delete=False` asegura que el archivo temporal no se elimine automáticamente cuando se cierre. 

A este archivo temporal `tempFile` se le aplica el método `read()` para leerlo y a su vez se obtiene la ruta del archivo temporal `tempFilePath`, almacenando todo esto en la variable `tempFilePath`.

```bash
            with tempfile.NamedTemporaryFile(delete=False) as tempFile:
                tempFile.write(file.read())
                tempFilePath = tempFile.name
```

A continuación, dentro del mismo ciclo for, se crea la variable `loader` que contendrá un objeto de la clase `PyPDFLoader`, `Docx2txtLoader` o `TextLoader` dependiendo de la extensión del archivo 'file'. El objeto generado será un documento que tendrá: 

* el contenido del archivo como una cadena de texto
* la metadata del archivo

```bash
            loader = None
            if fileExtension == ".pdf":
                loader = PyPDFLoader(tempFilePath)
            elif fileExtension == ".docx" or fileExtension == ".doc":
                loader = Docx2txtLoader(tempFilePath)
            elif fileExtension == ".txt":
                loader = TextLoader(tempFilePath)
```

Lo siguiente es un ciclo if, donde si `loader` contiene un objeto, se carga el contenido de ese objeto (texto y metadatos) a la variable 'text' y se borra el archivo temporal. De este modo la variable 'text' contendrá una lista de documentos con su texto y su metadata (etiquetas, nombres de archivo). 

 ```bash
            if loader:
                text.extend(loader.load())
                os.remove(tempFilePath)
```

Finalizado esta ejecución para un archivo, este bucle for vuelve a recorrerse para todos los archivos cargados.

Finalizado el bucle for para todos los archivos, se instancia un objeto de la clase `CharacterTextSplitter`, con los siguientes argumentos:

* **separator**: en este caso, se usa "\n" como separador, lo que significa que cada fragmento será separado por dos saltos de línea consecutivos.  
* **chunk_size**: es el tamaño máximo deseado para cada fragmento. En este caso, se establece el tamaño máximo en 1000 caracteres.  
* **chunk_overlap**: es el número de caracteres que se solapan entre dos fragmentos adyacentes. En este caso, se establece el overlap en 100 caracteres.  
* **length_function**: es la función que se utilizará para medir la longitud de cada fragmento. En este caso, se utiliza la función integrada `len()` para contar el número de caracteres en cada fragmento.

Luego, la función `split_documents()` recibe la cadena de texto original y la divide en fragmentos según los parámetros especificados en la instancia de `CharacterTextSplitter`. El resultado es una lista de fragmentos de texto, donde cada fragmento tiene un tamaño menor o igual al valor especificado en `chunk_size`. Si un fragmento supera el tamaño máximo, se dividen en varios fragmentos menores y se agregan a la lista resultante.

 ```bash
        textSplitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        textChunks = textSplitter.split_documents(text)
```

En el siguiente paso de la ejecución del código, se carga el modelo que permite generar las representaciones numéricas de texto, llamadas **embeddings**. Para mejorar el procesamiento de los datos para la creación de los mismos, se aprovechan las ventajas de utilizar una tarjeta gráfica, es decir, el procesamiento en GPU. Para ello, se define el parámetro `device` como 'cuda'.

El modelo utilizado para la creación de los embeddings se utiliza el modelo **all-MiniLM-L6-v2**, el cuál asigna frases y párrafos a un espacio vectorial denso de 384 dimensiones y puede utilizarse para tareas como la agrupación o la búsqueda semántica.

 ```bash
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                           model_kwargs={'device': 'cuda'})
```

Los embeddings creados son almacenados en una base de datos vectorial. En este caso se utiliza la clase FAISS (Facebook AI Similarity Search) que es una biblioteca para la búsqueda eficiente de similitudes y la agrupación de vectores densos. Contiene algoritmos que buscan en conjuntos de vectores de cualquier tamaño, hasta los que posiblemente no quepan en la RAM. También contiene código de apoyo para la evaluación y el ajuste de parámetros. 

Esto crear un objeto `VectorStore` mediante la función `from_documents()`, la que toma dos argumentos: 

* una lista de objetos Document, en este caso `textChunks` que es una lista de cadenas de caracteres que representan las diferentes partes del texto que se desea indexar. Cada cadena corresponde a un fragmento del texto original.  
* un objeto Embeddings que contiene información sobre cómo codificar el texto en vectores numéricos.

 ```bash
        vectorStore = FAISS.from_documents(textChunks, embedding=embeddings)
```

Este objeto `vectorStore` se usa en la función `createConversationalChain` y se instancia en una variable 'chain'.

```bash
        chain = utils.createConversationalChain(vectorStore)```
```

La función `createConversationalChain` crea una cadena de conversaciones para generar respuestas basadas en el contexto del chat. Utiliza un modelo de lenguaje (LLM) para generar texto y un recuperador para responder según el contexto. Además, utiliza una memoria para almacenar las conversaciones previas y ayudar a mejorar la comprensión del contexto.

Esta función comienza inicializando una cadena de conversaciones llamando a la clase `ConversationalRetrievalChain`. Esta clase es parte de la biblioteca de Python transformers, utilizada para implementar modelos de lenguaje y procesamiento de lenguaje natural.

En esta función primero se define un "pipeline" de trabajo que proporciona la librería transformers, que es la forma más fácil de usar un modelo preentrenado para una tarea dada. En esta "pipeline" se configuran los parámetros específicos para la generación de texto, la búsqueda y la gestión de memoria. Estos parámetros incluyen:

* la temperatura del modelo de lenguaje  
* el tipo de cadena de conversaciones  
* el número máximo de nuevas tokens permitidas  
* si se debe realizar muestreo  
* el número de secuencias de regresión deseadas  
* el identificador del token de fin de oración  

A continuación, se instancia el modelo `llm` ya instanciado y con las características definidas anteriormente.

Para generar guardar en memoria todo el historial de la conversación se utiliza `ConversationBufferMemory`. Luego, para utilizar ese hitorial se utiliza `ConversationalRetrievalChain` que combina el historial de chat y la pregunta en una pregunta independiente, busca los documentos relevantes en el recuperador y, por último, pasa esos documentos y la pregunta a una cadena de respuesta de preguntas para obtener una respuesta.

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

Por último, se llama a la función `displayChatHistory`, pasándole de argumento la cadena de conversaciones generada anteriormente.

```bash
        utils.displayChatHistory(chain)
```

La función `displayChatHistory` muestra una interfaz de chat para interactuar con una cadena de conversación y ver el historial de chat, la cual incluye las consultas de los usuarios y las respuestas del sistema en un formato de conversación.

Como argumentos utiliza 'chain', instanciada previamente, que toma un diccionario con una pregunta
y 'chat_history' como entrada, y devuelve un diccionario con una respuesta.

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

Esta función `displayChatHistory` utiliza a la función `conversationChat`, la cual tiene varios componentes importantes:

* result = chain({"question": query, "chat_history": history}): donde llama toma 'chain' que contiene la pregunta actual (query) y el historial de conversación anterior (history) y devuelve un resultado que incluye la respuesta a la pregunta actual.  
* history.append((query, result["answer"])): permite agregar la pregunta actual y su respuesta correspondiente al final del historial de conversación.
* return result["answer"]: devuelve solo la respuesta a la pregunta actual.

```bash
def conversationChat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]
```