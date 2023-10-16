# Pinecone + Colab + df - Documentación del Código

Este archivo README tiene como objetivo proporcionar una descripción detallada del código implementado en Google Colab para cargar documentos en Pinecone y llevar un registro de documentos cargados en un DataFrame (df) con metadatos. El código se divide en varias partes, lo que facilita su comprensión y ejecución.

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Resultados](#resultados)

## Introducción

Este código se enfoca en la carga de documentos en una base de datos vectorial en Pinecone y el seguimiento de la carga documental en un DataFrame (df) con metadatos. También se realiza una consulta de prueba a través del modelo Llama 2.

El código se ejecuta en varios pasos que se describen a continuación. Estos pasos permiten la carga de datos en Pinecone y en un DataFrame (df) con metadatos. Además, se proporciona información sobre las librerías a instalar y cómo consultar la base de datos vectorial en Pinecone.

## Instalación

### Paso 1. Instalar las librerías necesarias

El primer paso del código se centra en la instalación de los paquetes necesarios. Esto incluye la instalación de bibliotecas como `langchain`, `pypdf`, `docx2txt`, `pinecone-client`, `huggingface_hub`, `sentence_transformers`, entre otras. Estas bibliotecas son esenciales para la carga y consulta documental, así como para el modelo de embeddings.

## Configuración

### Paso 2. Importar las librerías necesarias

En esta sección, se importan las librerías requeridas para el proceso. Esto incluye la carga de documentos, la manipulación de texto, la configuración de Pinecone y la inicialización de un modelo de embeddings.

## Uso

# PARTE 1. BASE DE DATOS VECTORIAL EN PINECONE Y SEGUIMIENTO DE CARGA DOCUMENTAL EN DF

### Paso 3. Conectar con Pinecone y configurar el índice

En este paso, el código se encarga de la inicialización de Pinecone y la configuración del índice. Esto implica proporcionar una clave de API y un entorno específico. A continuación, se muestra un ejemplo de cómo realizar esta configuración:

```python
pinecone.init(api_key='api_key', environment='gcp-starter')
index_name = 'langchain-pinecone-llama2'  # Nombre del índice

# Crear un índice si no existe
if pinecone.list_indexes() == []:
    pinecone.create_index(name=index_name, dimension=384, metric='cosine')

# Conectar al índice
index = pinecone.Index(index_name=index_name)
```

### Paso 4. Definir modelo de embeddings y método de split

En este paso, se descarga un modelo de embeddings de HuggingFace que se utilizará para procesar los documentos y se define un método de split. Esto se realiza de la siguiente manera:

```python
print('Inicia descarga de modelo de embeddings de HuggingFace')
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
print('Modelo descargado')

# Definir el método de split para dividir el texto en fragmentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len, separators=['.\n\n', '.\n', '.', '\n\n', ',', ' '])
```

### Paso 5: Cargar los datos en Pinecone (vectores y text) y en df (metadata)

En este paso, se realiza la carga de datos en Pinecone para los vectores y en un DataFrame (df) para los metadatos. Esto incluye la extracción de texto, la manipulación de metadatos y la creación de un nuevo ítem en el DataFrame. Cada nuevo archivo se carga en una nueva fila del df, y se carga en 'n' cantidad de filas en la db de Pinecone, dependiendo la cantidad de fragmentos en las que fue dividido el archivo. Además, al cargar un nuevo archivo, este pasará de la carpeta de 'carga-documentos' a la carpeta 'documentos-cargados'. El siguiente ejemplo muestra cómo se lleva a cabo este proceso:

```python
# Montar la unidad de Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Establecer la ruta actual
ruta_actual = os.getcwd()

# Directorio que contiene los archivos
ruta_carga_documentos = os.path.join(ruta_actual, 'carga-documentos')

# Cargar el DataFrame si ya existe, de lo contrario, crear uno vacío
if os.path.exists('documentos_df.csv'):
    df = pd.read_csv('documentos_df.csv')
else:
    df = pd.DataFrame(columns=['nombre', 'ruta', 'formato', 'texto', 'fecha', 'hora', 'usuario'])

# Crear un conjunto con los nombres de archivo ya cargados
archivos_cargados = set(df['nombre'])

# Recorrer los archivos en el directorio carga-documentos
for archivo in os.listdir(ruta_carga_documentos):
    if archivo.endswith((".txt", ".docx", ".pdf")):
        if archivo not in archivos_cargados:
            # Procesar el archivo y cargarlo en Pinecone y en el DataFrame
          ruta_completa = os.path.join(ruta_carga_documentos, archivo)
          if archivo.endswith(".txt"):
              formato = ".txt"
              loader = TextLoader(ruta_completa, autodetect_encoding=True)
          elif archivo.endswith(".docx"):
              formato = ".docx"
              loader = Docx2txtLoader(ruta_completa)
          elif archivo.endswith(".pdf"):
              formato = ".pdf"
              loader = PyPDFLoader(ruta_completa)
          else:
              formato = "Desconocido"

          # Metadatos
          fecha_carga = date.today()
          hora_carga = datetime.datetime.now().time()
          usuario_carga = 'SD'

          # Carga en Pinecone
          data = loader.load()
          docs=text_splitter.split_documents(data)
          for i in range(len(docs)):
                docs[i].page_content = docs[i].page_content.replace('\n', '')
          docsearch=Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)

          # Extracción de texto limpio (data es una lista de tuplas: [(page_content, metadata)])
          texto = ''
          for i in range(len(data)):
            texto += ' ' + data[i].page_content.replace('\n', ' ')

          # Agregar nueva fila al DataFrame
          nueva_fila = {'nombre': archivo,
                        'ruta': ruta_completa,
                        'formato': formato,
                        'texto': texto,
                        'fecha': fecha_carga,
                        'hora': hora_carga,
                        'usuario': usuario_carga}
          df2 = pd.DataFrame([nueva_fila])
          df = pd.concat([df, df2], ignore_index=True)

          # Mueve el archivo a carpeta documentos-cargados
          ruta_documentos_cargados = os.path.join(ruta_carga_documentos, 'documentos-cargados')
          shutil.move(ruta_completa, ruta_documentos_cargados)

        else:
          # Si el archivo ya había sido cargado, se elimina del directorio carga-documentos
          ruta_completa = os.path.join(ruta_carga_documentos, archivo)
          os.remove(ruta_completa)

# Guardar el DataFrame en un archivo CSV
df.to_csv('documentos_df.csv', index=False)
```

### Paso 6: Consultar Base de Datos Vectorial Pinecone

Para consultar la base de datos vectorial en Pinecone, puedes seguir los siguientes pasos. Primero, verifica que el índice que creaste anteriormente esté disponible:

```python
pinecone.list_indexes()

# Si deseas traer los vectores desde un índice de Pinecone existente puedes hacerlo así:
docsearch = Pinecone.from_existing_index(index_name, embeddings)

```

# PARTE 2. CONSULTA DE LA BASE DE DATOS A TRAVÉS DEL MODELO LLAMA 2
### Paso 9: Consultar los documentos en dos pasos

La consulta de documentos se hará en dos pasos:

* Buscar similitud entre Query y Documentos para seleccionar los k documentos más pertinentes.

* Obtener la respuesta a la consulta utilizando el modelo Llama 2, basándose en la información obtenida de los k documentos seleccionados.

Autenticación en HuggingFace
Antes de continuar, asegúrate de autenticarte en HuggingFace con la siguiente función:

```python
from huggingface_hub import notebook_login
notebook_login()
```

### Paso 10. Cuantización y descarga del modelo Llama 2

Configura la cuantización para utilizar Llama 2 con menos memoria de GPU. Esto se hace de la siguiente manera:

```python
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

bnb_config = transformers.BitsAndBytesConfig(
     load_in_4bit=True,
     bnb_4bit_quant_type='nf4',
     bnb_4bit_use_double_quant=True,
     bnb_4bit_compute_dtype=bfloat16
)

model_id = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=True)

model = AutoModelForCausalLM.from_pretrained(model_id, device_map='auto', torch_dtype=torch.bfloat16, use_auth_token=True, local_files_only=False, quantization_config=bnb_config, trust_remote code=True)

pipe = pipeline("text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=4096
)
llm = HuggingFacePipeline(pipeline=pipe, model_kwargs={'temperature': 0.02})
```

# Paso 11. Ejecución con Pinecone
Carga el modelo Llama 2 y procede con la ejecución. Aquí se muestra cómo configurar la cadena (chain) y realizar la consulta:

```python
chain = load_qa_chain(llm, chain_type="stuff")
query = '¿En qué consiste la demanda contra la Provincia de San Luis?'
docs = docsearch.similarity_search(query, k=4)
answer = chain.run(input_documents=docs, question=query)
```

## Resultados

Esta sección muestra ejemplos de resultados obtenidos al ejecutar el código. Incluye fragmentos de texto y respuestas a consultas realizadas.

### Ejemplo 1

```python
translator = Translator()
translation = translator.translate(answer, src='en', dest='es')
answer =translation.text
answer
```
```plaintext
La demanda presentada por la administración de Parques Nacionales contra la provincia de San Luis busca declarar la inconstitucionalidad de la ley local V -0721-2010, que fue promulgada por el decreto ejecutivo provincial 1520 -MgJyc -2010 y declarado de utilidad pública y asuntoPara expropiar los derechos previamente cedidos por la provincia al ciudadano estatal sobre las propiedades inmuebles afectadas, con el objetivo de restaurarlos a sus propietarios originales y ancestrales, el pueblo nación Huarpe de San Luis, para la preservación y gestión sostenible de esa región.
```
```python
print('basado en los fragmentos:')
docs
```
```plaintext
basado en los fragmentos:
[Document(page_content='.499 y 18 y subsiguientes de la Ley General de Expropiaciones de la Provincia de San Luis V -0128-2004 (5497).     II) A fs. 446/449 del incidente sobre medida cautelar (CSJ 642/2010  (46-A)/CS1/IN9) se declaró la competencia originaria de esta Corte para entender en el caso, se admitió la prohibición de innovar requerida en forma previa a la promoción de la demanda, y,  en ese marco, se le ordenó a la Provincia de San Luis que se abstenga de ejecutar la ley local V -0721-2010 y toda otra disposición dictada en consecuencia, y de llevar a cabo actos que alteren la situación anterior a la sanción de esa norma. Asimismo, se ordenó la acumulación a este proceso de los autos caratulados “Gobierno de la Provincia de San Luis c/ Estado Nacional – Administración de Parques Nacionales s/'),
 Document(page_content='. 747/2010) ante el Juzgado Federal de la ciudad de San Luis, y describe las actuaciones llevadas a cabo en ese proceso.    Aduce que la esc rituración pendiente de las parcelas que componen el parque nacional constituye el aparente fundamento de la Provincia de San Luis para considerar que puede ignorar la calidad de dominio público federal que tienen las tierras en debate y su consecuente inc ompatibilidad con el régimen expropiatorio.    Pone de resalto  que la Administración de Parques Nacionales cumple desde hace años su función de custodia y administración en Sierra de las Quijadas. Considera que ello determina la condición dominical de carác ter público y que tal'),
 Document(page_content='.    5°) Que, ahora bien, esta Corte ha señalado que “los actos de las legislaturas provinciales no pueden ser invalidados sino en los casos en que la Cons titución concede al Congreso Nacional, en términos expresos, un poder exclusivo, o en que el ejercicio de idénticos poderes ha sido expresamente prohibido a las provincias, o cuando hay una absoluta y directa incompatibilidad en el ejercicio de ellos por e stas últimas” (Fallos: 331:1412 y sus citas, entre otros).    El conflicto que se ha suscitado entre la Administración de Parques Nacionales y la Provincia de San Luis, tiene como contexto la interacción de las competencias federales y locales, según la dis tribución que resulta del art ículo 75, inciso 30, de la Constitución Nacional, y exige determinar el alcance de lo dispuesto en dicha cláusula, conforme a lo que'),
 Document(page_content='. 6/33 la Administración de Parques Nacionales promueve demanda contra la Provi ncia de San Luis, a fin de que se declare la inconstitucionalidad de la ley local V -0721-2010, promulgada por el decreto del Poder Ejecutivo p rovincial 1520 -MGJyC-2010, que declaró de utilidad pública y sujetos a expropiación los derechos previamente cedid os por la demandada al Estado Nacional sobre los inmuebles afectados al funcionamiento del Parque Nacional Sierra de las Quijadas, manteniendo su status jurídico de área natural protegida, a los efectos de restituirlos “ a sus ancestrales y originarios pobladores, el Pueblo Nación Huarpe de San Luis, para la preservación y manejo sustentable de dicha región ”. Asimismo, solicita que se ordene la escrituración de esos inmuebles a su nombre')]
```

### Ejemplo 2
```python
query='¿Quiénes integran el juzgado de primera instancia 6, y con qué cargos?'
docs=docsearch.similarity_search(query, k=2)
answer = chain.run(input_documents=docs, question=query)
translator = Translator()
translation = translator.translate(answer, src='en', dest='es')
answer = translation.text
answer
```
```plaintext
La respuesta a esta pregunta se puede encontrar en el último párrafo del texto, donde se afirma que "iv) A fs. 224/228 SE presente Comunidad Huarpe de Guanacache A los efectos de ser tenida por parte en el proceso en los términosDel Artículo 90, Inciso 1 °, Del Código Procesal civil y Comercial de la Nacia ".Por lo tanto, los jueces de la Primera Instancia 6 son los miembros de la Comunidad Huarpe de Guanacache.
```
```python
print('basado en los fragmentos:')
docs
```
```plaintext
basado en los fragmentos:
[Document(page_content='- 26 - y en él funciona un establecimiento de utilidad nacional. Ello es así pues en virtud de las previsiones contenidas en el artículo 75, inciso 5° de la Ley Fundamental, es facultad del Congreso de la Nación disponer del uso y de la enajenación de tierras de propiedad nacional (Fallos: 276:104; 323:4046 y 327:429).    14) Que las consideraciones precedentes son suficientes para resolver el caso y tornan innecesario el tratamiento de los restantes argumen tos expuestos por las partes.  Por ello, y habiendo dictaminado la señora Procuradora General de la Nación, se resuelve: I. Hacer lugar a la demanda entablada por la Administración de Parques Nacionales y, en consecuencia, declarar la inconstitucionalidad de la ley V -0721-2010 de la Provincia de San Luis. II'),
 Document(page_content='. Agrega que el derecho a la posesión y propiedad comunitaria reviste una importancia fundamental, no solo por el significado que tiene la tierra para las culturas indígenas, sino también por el despojo sufrido por las comunidades a lo largo de la historia.    Solicita asimismo que se declare la procedencia de la compensación del crédito que pudiera resultar a favor del Estado Nacional en virtud de la expropiaci ón dispuesta, con las deudas que mantendría con la Provincia de San Luis y, a esos efectos, enumera una serie de juicios que tramitan ante esta Corte en los que ha formulado distintos reclamos de contenido económico.    IV) A fs. 224/228 se presenta Comunid ad Huarpe de Guanacache a los efectos de ser tenida por parte en el proceso en los términos del artículo  90, inciso 1°, del Código Procesal Civil y Comercial de la Nación.')]
```
