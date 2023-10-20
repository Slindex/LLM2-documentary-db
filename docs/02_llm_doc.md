# LangChain para chatear con documentos

```bash
# Dependencias necesarias
!pip install langchain
```

## Introducción

LangChain es un framework para el desarrollo de aplicaciones basadas en modelos del lenguaje. Permite aplicaciones que:

*    **Sean conscientes del contexto**: es decir, que conecten un modelo lingüístico a fuentes de contexto (instrucciones, ejemplos, contenido en el que basar su respuesta, etc.).
*    **Razonen**: es decir, que se basen en un modelo del lenguaje para razonar (sobre cómo responder basándose en el contexto proporcionado, qué acciones tomar, etc.).

Los principales puntos de valor de LangChain son:

*    **Componentes**: abstracciones para trabajar con modelos de lenguaje, junto con una colección de implementaciones para cada abstracción. Los componentes son modulares y fáciles de usar, tanto si se utiliza el resto del framework LangChain como si no.
*    **Cadenas estándar**: un conjunto estructurado de componentes para realizar tareas específicas de alto nivel.

Las cadenas estándar facilitan los primeros pasos. Para aplicaciones complejas, los componentes facilitan la personalización de las cadenas existentes y la creación de otras nuevas.

Para entender algunos de estos conceptos se plantean ejemplos sencillos para comprender sus aplicaciones. Para ello, se necesita en primer lugar, conectar con Google Drive para acceder a documentos.

## Generación Aumentada por Recuperación

Muchas aplicaciones LLM requieren datos específicos del usuario que no forman parte del conjunto de entrenamiento del modelo. La principal forma de conseguirlo es a través de la **Generación Aumentada por Recuperación** (Retrieval Augmented Generation - RAG). En este proceso, los datos externos se recuperan y se pasan al LLM cuando se realiza el paso de generación.

LangChain proporciona todos los bloques de construcción para aplicaciones RAG, desde las más sencillas a las más complejas. En el siguiente esquema se muestran dichos bloques:

<p align=center>
<img src="src/01_RAG.jpg">
<p>

## Carga de documentos

Se pueden cargar documentos de muchas fuentes diferentes. LangChain proporciona más de 100 cargadores de documentos diferentes, así como hacer integraciones con otros proveedores importantes del sector, como AirByte y Unstructured. LangChain proporciona integraciones para cargar todo tipo de documentos (HTML, PDF, código) desde todo tipo de ubicaciones (cubos s3 privados, sitios web públicos).

Se utilizan **loader** (cargadores de documentos) para cargar datos de una fuente como `Documents`. Un Document es un fragmento de texto y metadatos asociados.

Los loader proporcionan un método de "carga" para cargar datos como Documents desde una fuente configurada. Opcionalmente, también implementan un método "lazy load" para la carga perezosa de datos en memoria.

Hay numerosos métodos para cargar todo tipo de documentos, en este [link](https://python.langchain.com/docs/modules/data_connection/document_loaders/) se describen diferentes formas de cargar archivos CSV, File Directory, HTML, JSON, Markdown y PDF. En este [link](https://integrations.langchain.com/) se amplían todas las posibles integraciones que ofrece langchain.

En este proyecto, para cargar documentos PDF se utilizó PyPDFLoader que lo convierte en un array de documentos, donde cada documento contiene el contenido de la página y los metadatos con el número de página.

```bash
# Dependencia necesaria para
!pip install pypdf
# Importaciones
from langchain.document_loaders import PyPDFLoader
# Creación de loader y carga
loader = PyPDFLoader("Medida_cautelar.pdf")
pages = loader.load_and_split()
# Visualización de las páginas
pages[0]
```

Una ventaja de este enfoque es que los documentos pueden recuperarse con números de página.

## División de documentos

Una parte fundamental de la recuperación es obtener sólo las partes relevantes de los documentos. Esto implica varios pasos de transformación para preparar mejor los documentos para la recuperación. Una de las principales es dividir (o chunking) un documento grande en trozos más pequeños. LangChain proporciona varios algoritmos diferentes para hacerlo, así como una lógica optimizada para tipos de documentos específicos (código, markdown, etc.).

Cuando se quiere tratar con trozos largos de texto, es necesario dividir ese texto en **chunks**. Aunque parezca sencillo, puede resultar muy complejo. Lo ideal es mantener juntos los fragmentos de texto semánticamente relacionados. Lo que significa "semánticamente relacionados" puede depender del tipo de texto. En este [link](https://python.langchain.com/docs/modules/data_connection/document_transformers/) se muestra varias formas de hacerlo para distintos tipos de documentos.

A un alto nivel, los divisores de texto funcionan de la siguiente manera:

1.    Se dicide el texto en pequeños fragmentos semánticamente significativos (a menudo frases).
2.    Se empieza a combinar estos trozos pequeños en un trozo más grande hasta alcanzar un cierto tamaño (medido por alguna función).
3.    Una vez que se alcance ese tamaño, hacer de ese trozo su propio fragmento de texto y comenzar a crear un nuevo trozo de texto con cierto solapamiento (para mantener el contexto entre los trozos).

Esto significa que hay dos ejes diferentes a lo largo de los cuales se puede personalizar un divisor de texto:

1.    Cómo se divide el texto
2.    Cómo se mide el tamaño del trozo

El divisor de texto recomendado es el `RecursiveCharacterTextSplitter`. Este divisor de texto toma una lista de caracteres e intenta crear chunks basándose en el primer carácter, pero si alguno es demasiado grande pasa al siguiente, y así sucesivamente. Por defecto, los caracteres que intenta dividir son ["\n\n", "\n", " ", " "]. Otra opción que se probó en el proyecto es: ['.\n\n', '.\n', '.', '\n\n', ',', ' '] donde se tiene en cuenta que exista un punto antes de un salto de línea para conservar el párrafo u oración completo.

Además de controlar sobre qué caracteres se puede dividir, también se pueden controlar algunas otras cosas:

*    **length_function**: es cómo se calcula la longitud de los chunk. Por defecto sólo cuenta el número de caracteres, pero es bastante común pasar un contador de tokens aquí.
*    **chunk_size**: es el tamaño máximo de los chunks (medido por la función length).
*    **chunk_overlap**: es el máximo solapamiento entre chunks. Puede ser bueno tener algo de solapamiento para mantener cierta continuidad entre los chunks (por ejemplo, hacer una ventana deslizante).
*    **add_start_index**: por si se debe incluir en los metadatos la posición inicial de cada trozo dentro del documento original.

```bash
# Importaciones
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Separación y trozado
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=250,
                                              length_function=len,
                                              separators=['\n\n', '.\n', ' ', ''])
text_chunks = text_splitter.split_documents(pages)
# Visualización de los primeros dos trozos
text_chunks[:2]
```

## Vectores y embeddings

Otra parte clave de la recuperación ha pasado a ser la creación de incrustaciones (embeddings) para los documentos. Las incrustaciones capturan el significado semántico del texto, lo que permite encontrar de forma rápida y eficaz otros fragmentos de texto similares. LangChain proporciona integraciones con más de 25 proveedores y métodos de incrustación diferentes, desde código abierto hasta API propietarias, lo que le permite elegir el que mejor se adapte a sus necesidades. LangChain proporciona una interfaz estándar, lo que le permite cambiar fácilmente entre modelos.

Los modelos de incrustación (modelo de embeddings) crean una representación vectorial de un fragmento de texto. Esto es útil porque significa que podemos pensar en el texto en el espacio vectorial, y hacer cosas como la búsqueda semántica donde buscamos piezas de texto que son más similares en el espacio vectorial.

La clase base Embeddings de LangChain proporciona dos métodos: uno para incrustar documentos y otro para incrustar una consulta. El primero toma como entrada varios textos, mientras que el segundo toma un único texto. La razón de tener estos dos métodos separados es que algunos proveedores de incrustación tienen diferentes métodos de incrustación para los documentos (para ser buscados) frente a las consultas (la propia consulta de búsqueda).

Para este proyecto se adoptó utilizar como modelo de embedding **all-MiniLM-L6-v2** dado que es uno de los mas utilizados para este tipo de proyectos, tiene una velocidad de encoding elevada cuando se utiliza una GPU V100, es un modelo liviano para utilizar en local y tiene una buena performance. En este [link](https://www.sbert.net/docs/pretrained_models.html) se puede consultar mas información sobre este y otros modelos para esta tarea. En este [link](https://integrations.langchain.com/embeddings) se presentan todas las integraciones posibles que ofrece langchain.

El modelo se puede descargar desde este [link](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

A continuación, se muestra como se puede instanciar el modelo de embeddings a partir de tenerlo descargado en local.

```bash
# dependencia necesaria
!pip install sentence-transformers
# Importaciones
from langchain.embeddings import SentenceTransformerEmbeddings
# Instanciar el modelo de embeddings
embeddings = SentenceTransformerEmbeddings(
                            model_name="./all-MiniLM-L6-v2",
                            model_kwargs={"device": "cpu"}) # Aquí se debe setear "cuda" para usar la GPU

```

A continuación, se muestra un ejemplo de cómo se convierte el texto y una consulta en embeddings. En el primer ejemplo, se ingresa un documento, que en este caso son pequeñas frases.

```bash
example_embedding_document = embeddings.embed_documents(["Hi there!",
                                                         "Oh, hello!",
                                                         "What's your name?",
                                                         "My friends call me World",
                                                         "Hello World!"])
# Cantidad de embeddings
len(example_embedding_document)
```
En este caso la cantidad de ejemplos será de 5. Para ver cómo son los embeddings, se puede hacer lo siguiente:

```bash
# Se observan cómo son los embedings para la primera frase
print(example_embedding_document[0])
```

Lo que se verá es lo siguiente: `[-0.09151115268468857, 0.02514776960015297, 0.002047202782705426, ..., 0.03842880204319954]`

En el caso de hacer una pregunta, el proceso de realizar los embeddings es similar.

```bash
embedded_query = embeddings.embed_query("What was the name mentioned in the conversation?")
print(embedded_query)
```
Se verá un vector similar al anterior.

## Almacenamiento vectorial

Con el auge de los embeddings, ha surgido la necesidad de bases de datos que permitan un almacenamiento y una búsqueda eficientes de estas incrustaciones. LangChain proporciona integraciones con más de 50 almacenes de vectores diferentes, desde los locales de código abierto hasta los propietarios alojados en la nube, lo que le permite elegir el que mejor se adapte a sus necesidades. LangChain expone una interfaz estándar, lo que le permite cambiar fácilmente entre los almacenes de vectores.

Una de las formas más comunes de almacenar y buscar datos no estructurados es incrustarlos y almacenar los vectores de incrustación resultantes, y luego, en el momento de la consulta, incrustar la consulta no estructurada y recuperar los vectores de incrustación (embeddings vectors) que sean "más similares" a la consulta incrustada. Un almacén de vectores (vector store) se encarga de almacenar los datos incrustados y de realizar la búsqueda de vectores. En el siguiente esquema se describe el flujo de almacenamiento y búsqueda.

<p align=center>
<img src="src/02_Vector_store.jpg">
<p>

Hay muchas grandes opciones de almacenes de vectores, Chroma, FAISS y Lance son opciones gratuitas, de código abierto, y se ejecutan completamente desde local.

En el siguiente [link](https://python.langchain.com/docs/modules/data_connection/vectorstores/) se puede consultar más información sobre los almacenamientos de vectores. En este [link](https://integrations.langchain.com/vectorstores) se presentan todas las integraciones pobibles que ofrece langchain.

Mas información sobre las bases de datos vectoriales en este [link](https://www.pinecone.io/learn/vector-database/).

### FAISS

FAISS (Facebook AI Similarity Search) es una biblioteca que permite a los desarrolladores buscar rápidamente incrustaciones de documentos multimedia que sean similares entre sí. Resuelve las limitaciones de los motores de búsqueda de consultas tradicionales, optimizados para búsquedas basadas en hash, y ofrece funciones de búsqueda de similitudes más escalables.

Mas información en este [link](https://ai.meta.com/tools/faiss/).

Para utilizar esta base de datos, se hace lo siguiente:

```bash
# Dependencias
!pip install faiss-cpu
# importaciones
from langchain.vectorstores import FAISS
```

Previamente se definió el modelo de embeddings y ya se cuenta con los fragmentos de texto que se quieren convertir en embeddings. A continuación, se hace dicha conversión y se guardan los mismos en una base de datos vectorial.

```bash
db_faiss = FAISS.from_documents(text_chunks, embeddings)
```

Es importante destacar que esta base de datos se guarda en memoria.

Ahora, es posible hacer consultas y buscar por similitud. Hay diversas formas de hacer esta búsqueda. A continuación, se muestran una de las formas: Búsqueda por similitud.

```bash
query = "Cuál es la medida cautelar"
docs = db_faiss.similarity_search(query)
# Se muestran los primeros 3 fragmentos similares que resultan de la búsqueda
docs[:3]
```

### Chroma

La ventaja de este almacenamiento es que se pueden guardar los embeddings en local y hacerlos persistentes.

Para utilizar esta base de datos, se hace lo siguiente:

```bash
# Dependencias
!pip install chromadb
# importaciones
from langchain.vectorstores import Chroma
# Creación de la base de datos
db_chroma = Chroma.from_documents(text_chunks, embeddings)
```
Luego se puede realizar la misma búsqueda por similitud que en el caso de FAISS.

### Pinecone

La base de datos vectorial [Pinecone](https://www.pinecone.io/) es una base de datos vectorial gestionada y nativa de la nube con una API sencilla y sin complicaciones de infraestructura. Pinecone ofrece resultados de consulta frescos y filtrados con baja latencia a escala de miles de millones de vectores. Puede tratar datos vectoriales de alta dimensión a mayor escala, fácil integración y resultados de consulta más rápidos.

Más información para conocer Pinecone en este [link](https://docs.pinecone.io/docs/overview#:~:text=Pinecone%20Overview&text=It's%20a%20managed%2C%20cloud%2Dnative,scale%20of%20billions%20of%20vectors.).

## Modelo del lenguaje

Para este proyecto se utilizó el modelo **LLaMA 2** (Large Language Model Meta AI), un gran modelo de lenguaje fundacional de última generación diseñado para ayudar a los investigadores a avanzar en su trabajo en este subcampo de la IA.

LLaMA está disponible en varios tamaños (7B, 13B, 70B parámetros). Los modelos más pequeños y de mayor rendimiento, permiten estudiar estos modelos a otros miembros de la comunidad investigadora que no tienen acceso a grandes cantidades de infraestructura, lo que democratiza aún más el acceso a este importante campo en rápida evolución.

Mas información sobre LLaMA 2 en este [link](https://ai.meta.com/blog/llama-2/) y en este [link](https://ai.meta.com/llama/).

Ahora, debido al enorme tamaño de los grandes modelos lingüísticos (LLM), la **cuantización** se ha convertido en una técnica esencial para ejecutarlos con eficacia. Al reducir la precisión de sus pesos, se puede ahorrar memoria y acelerar la inferencia, conservando al mismo tiempo la mayor parte del rendimiento del modelo. Recientemente, la cuantización de 8 y 4 bits ha abierto la posibilidad de ejecutar LLM en hardware de consumo. Junto con las técnicas de parámetros eficientes para afinarlos (LoRA, QLoRA), esto creó un rico ecosistema de LLM locales que ahora compiten con GPT-3.5 y GPT-4 de OpenAI.

En la actualidad, existen tres técnicas principales de cuantificación: NF4, GPTQ y GGML. GGML es una biblioteca en C centrada en el aprendizaje automático. Fue creada por Georgi Gerganov, de ahí las iniciales "GG". Esta biblioteca no solo proporciona elementos fundacionales para el aprendizaje automático, como los tensores, sino también un formato binario único para distribuir LLM. La ventaja de este tipo de modelos es que se pueden descargar y ejecutar en una CPU.

Mas información sobre los modelos ggml en este [link](https://mlabonne.github.io/blog/posts/Quantize_Llama_2_models_using_ggml.html).

Para este proyecto se adoptó el uso del modelo mas pequeño 7B dada las limitaciones de recursos para la investigación y, en particular, para la investigación se utilizó el modelo cuantizado [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf). Este es el modelo 7B afinado, optimizado para casos de uso de diálogo y convertido para el formato de transformadores de Hugging Face.

Para poder utilizar este modelo se usa la librería [CTransformers](https://python.langchain.com/docs/integrations/llms/ctransformers) dentro de LangChain.

```bash
# Dependencias necesarias
! pip install ctransformers
# Importaciones
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# Instanciación del modelo
llm = CTransformers(model="./llama-2-7b-chat.ggmlv3.q4_0.bin",
                        streaming=True,
                        callbacks=[StreamingStdOutCallbackHandler()],
                        model_type="llama", 
                        config={'temperature': 0.01}, 
                        n_ctx=1024, max_tokens= 0)
```

## Recuperadores (Retrivers)

Un recuperador (retriver) es una interfaz que devuelve documentos a partir de una consulta no estructurada. Es más general que un almacén vectorial. Un recuperador no necesita ser capaz de almacenar documentos, sólo de devolverlos (o recuperarlos). Los almacenes vectoriales pueden ser la columna vertebral de un recuperador, pero también existen otros tipos de recuperadores.

Una vez que los datos están en la base de datos, hay que recuperarlos. LangChain admite muchos algoritmos de recuperación diferentes, desde la búsqueda semántica simple hasta una serie de algoritmos para aumentar el rendimiento.

Hasta ahora, se hicieron tres pasos principales luego de cargar un documento:

1.    Dividir los documentos en trozos
2.    Creación de embeddings para cada documento
3.    Almacenamiento de documentos y embeddings en un almacén vectorial

Luego de que se almacena en una base de datos, se genera por detrás unos índices los cuales se pueden exponer a la interfaz de recuperación, permitiendo de este modo obtener una respuesta a una pregunta.

Un índice es una estructura de datos que permite realizar búsquedas eficientes, y un recuperador es el componente que utiliza el índice para encontrar y devolver documentos relevantes en respuesta a la consulta de un usuario. El índice es un componente clave en el que se basa el recuperador para realizar su función.

Más información sobre retrival/index en este [link](https://python.langchain.com/docs/modules/data_connection/retrievers/) y en este [link](https://blog.langchain.dev/retrieval/).

El proceso para convertir datos brutos no estructurados en una cadena de control de calidad es el que se muestra en el siguiente esquema:

<p align=center>
<img src="src/03_Chat_flow.jpeg">
<p>

En **Output** un LLM produce una respuesta utilizando un indicador que incluye la pregunta y los datos recuperados. 

A continuación, se crean los índices y se hace una pregunta utilizando `RetrievalQA` que es el recuperador más simple para preguntas y respuestas.

```bash
# Importaciones
from langchain.chains import RetrievalQA
# Creación de los índices usando en este caso Chroma
retriever = db_chroma.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=retriever)
# Pregunta
query = "Qué impone la Disposición Nº 218/06?"
# Recuperación de la respuesta
qa.run(query)
```

Mas información sobre Preguntas/Respuestas sobre documentos en este [link](https://js.langchain.com/docs/use_cases/question_answering/).

## Conversación avanzada

Conversar con los LLM es una excelente manera de demostrar sus capacidades. Añadir memoria, el historial de chat y el contexto externo puede aumentar exponencialmente la complejidad de la conversación. Para mas información sobre conversación avanazada se puede ver este [link](https://js.langchain.com/docs/use_cases/question_answering/advanced_conversational_qa).

Por otra parte, se pueden crear los Agentes Recuperadores de la Conversación, que se trata de un agente optimizado específicamente para realizar recuperaciones cuando sea necesario mientras se mantiene una conversación y poder responder a preguntas basadas en diálogos anteriores en la conversación. Mas información en este [link](https://js.langchain.com/docs/use_cases/question_answering/conversational_retrieval_agents).

Es importante destacar que no se llegó a elaborar este punto en el alcance del proyecto, pero se recomienda fuertemente examinarlo en próximas etapas.
