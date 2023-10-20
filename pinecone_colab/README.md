# Pinecone + Colab + df - Documentación del Código

Este archivo README tiene como objetivo proporcionar una descripción detallada del código implementado en Google Colab para cargar documentos en Pinecone y llevar un registro de documentos cargados en un DataFrame (df) con metadatos. El código se divide en varias partes, lo que facilita su comprensión y ejecución.

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Resultados](#resultados)

## Introducción

Este código se enfoca en la carga de documentos en una base de datos vectorial en Pinecone y el seguimiento de la carga documental tanto en un DataFrame (df) con metadatos como en la propia db de Pinecone que también admite metadatos.

También se realiza una consulta de prueba a través del modelo Llama 2.

El código se ejecuta en varios pasos que se describen a continuación. Estos pasos permiten la carga de datos en Pinecone y en un DataFrame (df) con metadatos. Además, se proporciona información sobre las librerías a instalar y cómo consultar la base de datos vectorial en Pinecone, incluyendo uso de operadores lógicos para filtrar los vectores.

## Instalación

### Paso 1. Instalar las librerías necesarias

El primer paso del código se centra en la instalación de los paquetes necesarios. Esto incluye la instalación de bibliotecas como `langchain`, `pypdf`, `docx2txt`, `pinecone-client`, `huggingface_hub`, `sentence_transformers`, entre otras. Estas bibliotecas son esenciales para la carga y consulta documental, así como para el modelo de embeddings.

## Configuración

### Paso 2. Importar las librerías necesarias

En esta sección, se importan las librerías requeridas para el proceso. Esto incluye la carga de documentos, la manipulación de texto, la configuración de Pinecone y la inicialización de un modelo de embeddings.

## Uso

# PARTE 1. BASE DE DATOS VECTORIAL EN PINECONE Y SEGUIMIENTO DE CARGA DOCUMENTAL

### Paso 3. Conectar con Pinecone y configurar el índice

En este paso, el código se encarga de la inicialización de Pinecone y la configuración del índice. Esto implica proporcionar una clave de API y un entorno específico. A continuación, se muestra un ejemplo de cómo realizar esta configuración:

```python
pinecone.init(api_key='api_key', environment='gcp-starter')
indexName = 'langchain-pinecone-llama2' # indexName del cliente

# Creación de index si no existe
if pinecone.list_indexes() == []:
  pinecone.create_index(name=indexName, dimension=384, metric='cosine')

# Conexión con index
index = pinecone.Index(index_name=indexName)
```

### Paso 4. Definir modelo de embeddings y método de split

En este paso, se descarga un modelo de embeddings de HuggingFace que se utilizará para procesar los documentos y se define un método de split. Esto se realiza de la siguiente manera:

```python
print('Inicia descarga de modelo de embeddings de HuggingFace')
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
print('Modelo descargado')

# Definir el método de split para dividir el texto en fragmentos
textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len, separators=['.\n\n', '.\n', '.', '\n\n', ',', ' '])
```

### Paso 5: Cargar los datos en Pinecone (vectores y text) y en df (metadata)

En este paso, se realiza la carga de datos en Pinecone para los vectores y metadatos, y en un DataFrame (df) en Pandas para llevar un registro de los archivos cargados junto a sus metadatos. Cada nuevo archivo se carga en una nueva fila del df, y se carga en 'n' cantidad de filas en la db de Pinecone, dependiendo la cantidad de fragmentos en las que fue dividido el archivo. Además, al cargar un nuevo archivo, este pasará de la carpeta de 'carga-documentos' a la carpeta 'documentos-cargados'.

Este proceso es complejo ya que el código aquí realiza varias acciones:
* Corroborar que el archivo no ha sido cargado anteriormente en Pinecone
* Extraer los metadatos tanto del archivo, como los de situación (categoría especificada, usuario que hace la carga, fecha y hora de carga, cantidad de fragmentos en los que se divide el archivo, etc.)
* Crear un diccionario para los metadatos en Pinecone, y un diccionario similar para las columnas del df.
* Mover los archivos hacia la carpeta 'documentos-cargados' en caso de que se hayan cargado satisfactoriamente y borrarlos advirtiendo previamente con un mensaje, en caso de que no se hayan cargado.

El siguiente ejemplo muestra cómo se lleva a cabo este proceso:

```python
# Montar la unidad de Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Establecer la ruta actual
%cd '/content/drive/MyDrive/Llama2+Pinecone+Langchain'
currentPath = os.getcwd()

# Directorio que contiene los archivos a cargar, y directorio que contiene los archivos cargados
documentsUploadPath = os.path.join(currentPath, 'carga-documentos')
loadedDocumentsPath = os.path.join(documentsUploadPath, 'documentos-cargados')

# Solicitar al usuario la entrada por teclado de metadatos situacionales (usuario que hace la carga, categoría de los archivos cargados)
user = ""
validOptions = ["Carla", "David", "Jeremías", "Jerson", "René", "Gonzalo", "Otro"]
while user not in validOptions:
    user = input('Elija el nombre del usuario que carga los documentos (Carla, David, Jeremías, Jerson, René, Gonzalo, Otro): ')

category = ""
validOptions = ["cv", "fallo judicial", "documentación", "literatura", "otros","carpeta 0","carpeta 1","carpeta 2",
                "carpeta 3","carpeta 4","carpeta 5","carpeta 6","carpeta 7","carpeta 8","carpeta 9","carpeta 10",
                "carpeta 11","carpeta 12","carpeta 13","carpeta 14","carpeta 15","carpeta 16"]
while category not in validOptions:
    category = input('Elija la categoría de los documentos a cargar (cv, fallo judicial, documentación, literatura, carpeta n (0 a 16), otros): ')


# Cargar el DataFrame si ya existe
if os.path.exists('documentos_df.csv'):
    df = pd.read_csv('documentos_df.csv')
else:
    # Si no existe, crea un DataFrame vacío
    df = pd.DataFrame(columns=['category', 'date', 'format', 'name', 'path', 'text', 'time', 'user'])

# Acceder a los registros de Pinecone para verificar archivos cargados
records = Pinecone.from_existing_index(indexName, embeddings)



# Recorrer los archivos en el directorio carga-documentos
for file in os.listdir(documentsUploadPath):
    if file.endswith((".txt", ".docx", ".pdf", ".PDF")): #, ".wav", ".mp4", ".csv"


        # Si el archivo no está cargado en Pinecone, se extrae el texto, los vectores y los metadatos, y se carga en df y en Pinecone
        record = records.similarity_search(query='a', k=1, filter= {"name" : {"$eq": f"{file}"}})
        if len(record) == 0:
          fullPath = os.path.join(documentsUploadPath, file)
          try:
            if file.endswith(".txt"):
                format = ".txt"
                loader = TextLoader(fullPath, encoding='UTF-8')
            elif file.endswith(".docx"):
                format = ".docx"
                loader = Docx2txtLoader(fullPath)
            elif file.endswith(".pdf"):
                format = ".pdf"
                loader = PyPDFLoader(fullPath)
            else:
                format = "Desconocido"

            # Extraer fecha y hora de carga del archivo
            date = date.today()
            time = datetime.datetime.now().time()

            # Carga en Pinecone
            data = loader.load()
            docs=textSplitter.split_documents(data)
            for i in range(len(docs)):
              docs[i].page_content = docs[i].page_content.replace('\n', '')
              docSearch = Pinecone.from_texts([docs[i].page_content], embeddings, index_name=indexName,
                                                metadatas = [{
                                                      'category': category,
                                                      'chunk_n': i+1,
                                                      'chunk_size': len(docs[i].page_content),
                                                      'chunks_total': len(docs),
                                                      'date': date,
                                                      'format': format,
                                                      'name': file,
                                                      'path': fullPath,
                                                      #'text': docs[i].page_content.replace('\n', ' '), # innecesario: 'text' se carga por defecto
                                                      'time': time.strftime("%H:%M:%S"),
                                                      'user': user
                                                  }])

            # Extracción de texto limpio (data es una lista de tuplas: [(page_content, metadata)])
            texto = ''
            for i in range(len(data)):
              texto += ' ' + data[i].page_content.replace('\n', ' ')

            # Agregar nueva fila al DataFrame
            newRow = {
                      'category': category,
                      'date': date,
                      'format': format,
                      'name': file,
                      'path': fullPath,
                      'text': texto,
                      'time': time,
                      'user': user
                      }
            df2 = pd.DataFrame([newRow])
            df = pd.concat([df, df2], ignore_index=True)

            # Mueve el archivo a carpeta documentos-cargados
            shutil.move(fullPath, loadedDocumentsPath)
            print(f'el archivo {file} fue cargado en Pinecone correctamente')
          except:
            os.remove(fullPath)
            print(f'No se pudo acceder al contenido del archivo {file}')


        else:
          # El archivo ya ha sido cargado, eliminarlo del directorio carga-documentos
          fullPath = os.path.join(documentsUploadPath, file)
          os.remove(fullPath)
          print(f'el archivo {file} ya se encontraba cargado en Pinecone')

# Guardar el DataFrame en un archivo CSV
df.to_csv('documentos_df.csv', index=False)
```

### Paso 6: Consultar Base de Datos Vectorial Pinecone

Para consultar la base de datos vectorial en Pinecone, puedes seguir los siguientes pasos. Primero, verifica que el índice que creaste anteriormente esté disponible:

```python
pinecone.list_indexes()

# Si deseas traer los vectores desde un índice de Pinecone existente puedes hacerlo así:
docSearch = Pinecone.from_existing_index(indexName, embeddings)

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

bnbConfig = transformers.BitsAndBytesConfig(
     load_in_4bit=True,
     bnb_4bit_quant_type='nf4',
     bnb_4bit_use_double_quant=True,
     bnb_4bit_compute_dtype=bfloat16
     )

modelId = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(modelId,use_auth_token=True)


model = AutoModelForCausalLM.from_pretrained(modelId,
                                            device_map='auto',
                                             torch_dtype=torch.bfloat16,
                                             use_auth_token=True,
                                             local_files_only=False,
                                             quantization_config=bnbConfig,
                                             trust_remote_code=True
                                            #cache_dir="model/"
                                            )

pipe = pipeline("text-generation",
            model=model,
            tokenizer= tokenizer,
            #torch_dtype=torch.bfloat16,
            #device_map="auto",
            max_new_tokens = 4096,
            #do_sample=True,
            #top_k=30,
            #num_return_sequences=1,
            #eos_token_id=tokenizer.eos_token_id
            )
llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0.02})
```

# Paso 11. Ejecución con Pinecone
Carga el modelo Llama 2 y procede con la ejecución. Aquí se muestra cómo configurar la cadena (chain) y realizar la consulta filtrando metadatos en caso de precisarlo:

```python
chain=load_qa_chain(llm, chain_type="stuff")
query='¿Qué dice MARCELA GAETE REYES del Programa “Mi Abogado” en calidad de representación de la víctima de autos?'
docs=docSearch.similarity_search(query, k=5, filter=
                                   {
                                    #'category': {'$eq': str},
                                    #'chunk_n': {'$gte': int},
                                    #'chunk_size': {'$gte': int},
                                    #'chunks_total': {'$gte': int},
                                    #'date': {'$eq': str},
                                    #'format': {'$eq': str},
                                    #'name': {'$eq': str},
                                    #'path': {'$eq': str},
                                    #'time': {'$eq': str},
                                    #'user': {'$eq': str}
                                    })
answer = chain.run(input_documents=docs, question=query)
```

## Resultados

Esta sección muestra ejemplos de resultados obtenidos al ejecutar el código. Incluye fragmentos de texto y respuestas a consultas realizadas.

### Ejemplo

```python
translator = Translator()
translation = translator.translate(answer, src='en', dest='es')
answer = translation.text
answer
```

```plaintext
Marcela Gaete Reyes, como representante de la víctima en el programa "Mi Abogado", afirma que la víctima es una niña de 13 años que fue sometida a situaciones abusivas por Mauricio Aguilera Valenzuela, la imputada.La madre de la víctima, Alejandra Martínez Groove, reanudó una relación romántica con los imputados, lo que llevó al abandono de la víctima de su hogar y que se quedara bajo el cuidado de su abuela.Esta situación facilitó el acceso de los imputados a los otros hermanos de la víctima, que ahora están en riesgo.Además, el hecho de que esta circunstancia podría influir en la retracción de la víctima cuando se vio privada de su contexto familiar en el que se desarrolló.
```

```python
print('basado en los fragmentos:')
docs
```
```plaintext
basado en los fragmentos:
[Document(page_content='. 140 dei Código Procesal Penal, esto es, la • necesidad de cautela, el imputado MAURICIO AGUILERA VALENZUELA, si bien, no presenta condenas anteriores por ilícito alguno, la naturaleza del delito tratándose de un delito de abuso sexual reiterado, tanto del 366 como del 366 quater, concurriendo además la circunstancia calificante del 368 estando el imputado al cuidado de la víctima, y las consecuencias que sus actos originaron en la víctima, hacen presumir que la libertad de este claramente constituye un peligro para la seguridad de la víctiniá y peligro para la seguridad de la sociedad, reconducido en este caso a peligro de fuga, dado principalmente, a que el imputado publicó én página web chile autos venta de su vehículo por viaje, donde además , pone en un peligro latente a la misma víctima o incluso a otras, y por otro lado, dada la 4 \t\tpenalidad qué arriesga por el delito reiterado que se le imputa, arriesga un cumplimiento efectivo de la misma', metadata={'category': 'carpeta 0', 'chunk_n': 58.0, 'chunk_size': 963.0, 'chunks_total': 325.0, 'date': datetime.date(2023, 10, 18), 'format': '.pdf', 'name': 'carp 3.pdf', 'path': '/content/drive/MyDrive/Llama2+Pinecone+Langchain/carga-documentos/carp 3.pdf', 'time': datetime.datetime(2023, 10, 18, 15, 46, 14), 'user': 'Gonzalo'}),
 Document(page_content='.....,.,, CAR1 TOMO, DELITOS GENERALES Y CUASIDELITOS TERMINADO DENUNCIANTE 14181453-2 ROBERTO OCTAVIO MARTINEZ CARIZ IMPUTADO VICTIMA VICTIMA 10781828-6 16247595-9 14181453-9 JORGE ANTONIO PINTO CARVAJAL FRANCiSCO ANDRES OLGUIN GUZMAN ROBERTO OCTAVIO MARNINEZ http://fnprodø  1/sao/ficha!busquedalextracto.php?Y2VkdWxhPTEOMTgxNDUzLTImZG... 02/10/2017', metadata={'category': 'carpeta 1', 'chunk_n': 289.0, 'chunk_size': 351.0, 'chunks_total': 428.0, 'date': datetime.date(2023, 10, 18), 'format': '.pdf', 'name': '1.0.pdf', 'path': '/content/drive/MyDrive/Llama2+Pinecone+Langchain/carga-documentos/1.0.pdf', 'time': datetime.datetime(2023, 10, 18, 13, 54, 59), 'user': 'Jeremías'}),
 Document(page_content='acción social, lo que fue interpretado como una plataforma para proyectar una postulación al concejo municipal de La Pintana. LOS MISTERIOS DE LA AUTOMOTORA El Parque Automotriz Vespucio San Ramón se ha convertido en el eje donde se cruzan distintos pérsonajes de la trama donde se teje el poder del alcalde Aguilera. Administrado por una sociedad de Marcela Rosales Belmar, la que paga a la municipalidad 200 UTM mensuales ($9,3 millones), CIPER detectó a más de 80 vendedores de autos que operan allí. Una de las sociedades que registra domicilio en la automotora es "Bastías y Zamorano y Compañía Limitada", cuyo socio Juan Carlos Bastías Olea registra condenas por narcotráfico. En 2010, Bastías fue condenado a 10 año§ por pertenecer a una red que digitaba traslados de cocaína de Anca a Santiago, utilizando para ello a mujeres adolescentes. En 1997 había sido condenado a cinco años y un día por tráfico de cocaína', metadata={'category': 'carpeta 1', 'chunk_n': 44.0, 'chunk_size': 921.0, 'chunks_total': 428.0, 'date': datetime.date(2023, 10, 18), 'format': '.pdf', 'name': '1.0.pdf', 'path': '/content/drive/MyDrive/Llama2+Pinecone+Langchain/carga-documentos/1.0.pdf', 'time': datetime.datetime(2023, 10, 18, 13, 54, 59), 'user': 'Jeremías'}),
 Document(page_content='.S. copia de los antecedentes de la carpeta de investigación en referencia, por el delito de ABUSO SEXUAL DEL 366 BIS Y 366 QUATER. En estos hechos la víctima es la menor de iniciales A.C.M. de 13 años de edad, el cual estaría siento sometida a circunstancias vuineradoras de sus derechos, ya que su madre ALEJANDRA MARTÍNEZ GROOVE, retomó la relación sentimental con el imputado MAURICIO AGUILERA VALENZUELA, por lo cual la menor, hizo abandono del hogar de su antecedentes domicilio (a familia, yéndose a vivir con su abuela, y se tienen además de que, este grupo familiar estaría pronto a cambiar de uno que sería arrendado por el imputado) lo que facilitaría el acceso del imputado a los otros 3 hermanos de la víctima, los que se encuentran en riesgo y esto sumado a que esta circunstancia, podría influir en la retractación de la víctima al verse privada del contexto familiar en el cual ella se desenvolvía', metadata={'category': 'carpeta 0', 'chunk_n': 164.0, 'chunk_size': 913.0, 'chunks_total': 562.0, 'date': datetime.date(2023, 10, 18), 'format': '.pdf', 'name': 'carp 2.pdf', 'path': '/content/drive/MyDrive/Llama2+Pinecone+Langchain/carga-documentos/carp 2.pdf', 'time': datetime.datetime(2023, 10, 18, 15, 48, 36), 'user': 'Gonzalo'}),
 Document(page_content=".2do. Gabriel Reyes Muftoz de esta dotación de esta Unidad, se traslada hasta el sector del Paradero Nro. 30 Camino Lonquén, Parcela N'ro. 44, Sector del Roto Chileno, Comuna de Talagante, con la finalidad de efectuar fijación fotográfióa del lugar Sindicado al aparecer por la víctima como sitio del Suceso.", metadata={'category': 'carpeta 0', 'chunk_n': 127.0, 'chunk_size': 308.0, 'chunks_total': 262.0, 'date': datetime.date(2023, 10, 18), 'format': '.pdf', 'name': 'carp 6.pdf', 'path': '/content/drive/MyDrive/Llama2+Pinecone+Langchain/carga-documentos/carp 6.pdf', 'time': datetime.datetime(2023, 10, 18, 15, 43, 55), 'user': 'Gonzalo'})]
```


## Es importante destacar que las acciones ejecutadas en la db de Pinecone mediante el código pueden ser visualizadas para mejor entendimiento a través del servicio web de Pinecone, en el cual por medio de una interfaz gráfica se puede acceder al contenido de los vectores y sus metadatos.
