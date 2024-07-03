<p align=center>
<img src="docs\src\Banner HP.png">
<p>

## Introducción

Los **Large Language Models** (LLMs) son modelos de inteligencia artificial diseñados para comprender y generar texto haciendo uso del **Natural Language Processing** (NLP), en español, Procesamiento del Lenguaje Natural. Los LLM pueden generar texto coherente y relevante, responder preguntas y realizar tareas basadas en el lenguaje, lo cual los dota de capacidades increíbles para abordar y solucionar múltiples problemáticas relacionadas a la interpretación y generación del lenguaje.

Una problemática presente en la actualidad es la alta dificultad existente al momento de consultar grandes bases de datos documentales, especialmente cuando la información requerida se encuentra segmentada en múltiples documentos. Mediante la implementación y el uso de los LLMs es posible desarrollar agentes basados en IA capaces de responder a una consulta hecha por un usuario utilizando diversas fuentes de información como referencia.

Este proyecto busca utilizar **LlaMa 2**, el LLM OpenSource más grande desarrollado hasta la fecha, con el fin de desarrollar una aplicación capaz de interpretar el contenido de múltiples archivos alojados en una base de datos documental. El contenido de estos archivos podrá ser consultado, accedido y resumido mediante el uso del **lenguaje natural** y contará con extensiones que almacenen texto **(.pdf, .txt, .md, etc...)**. Además, esta aplicación podrá responder consultas complejas que requieran acceder a la información de múltiples documentos.

## Contexto

Este proyecto se desarrolla como una pasantía empresarial para la empresa **Go Up Cloud** y, a su vez, como proyecto grupal de grado para el Bootcamp **Soy Henry**. Por lo tanto, la construcción de la aplicación propuesta dentro de los lineamientos y alcances del proyecto tendrá principalmente fines de investigación y desarrollo de productos basados en LLMs con potencial de derivar en una solución comercial que pueda ser desarrollada y utilizada a criterio, conveniencia y disposición por la empresa **Go Up Cloud**. El desarrollo de este proyecto se planea en el intervalo de tiempo de 1 mes.

## Alcance del proyecto de investigación

El campo de acción de este proyecto contempla tanto la **investigación** sobre la aplicación de la tecnología LLaMa 2 así como la creación, desarrollo y configuración de un Producto Mínimo Viable (MVP) o **Prototipo de un servicio web** que use Llama2 como modelo de IA pre-entrenado para realizar consultas inteligentes a una base de datos documental. Este proyecto integra múltiples tecnologías Open Source de libre uso comercial, así como otras de libre uso personal para la creación de este MVP. Este proyecto contempla además la elaboración de documentación referente al funcionamiento del mismo, así como un video demostrativo en el que se detalla su uso en la práctica.

## Tecnologías utilizadas

Se utilizaron las siguientes tecnologías para el desarrollo de este proyecto de investigación:

*    **Gestión de proyecto**: AzureDevOps
*    **Repositorio**:  GitHub
*    **Entorno de testing**: Google Colab Pro
*    **LLM**: LlaMa 2
*    **Hub de LLMs**: Hugging Face, Replicate
*    **Framework LLM**: LangChain
*    **Embeddings**: Transformers
*    **Base de datos Vectorial**: Pinecone, Chroma, FAISS
*    **Deploy testing**: Streamlit
*    **Framework web**: Django
*    **Servicio de Nube**: Azure
*    **Contenedor**: Docker

## Etapas de Desarrollo

Este proyecto consta de 4 grandes etapas de desarrollo, cada una pensada para añadir funcionalidades al modelo de forma incremental.

### Desarrollo e Implementación del LLM

En esta primer etapa se realizaron tareas de investigación sobre los Modelos Grandes del Lenguaje (LLM), su funcionamientos, casos de aplicación, documentación disponible, frameworks de trabajo, etc. Con esta infromación se elaboró un [Resumen del Marco Teórico]() a partir de una lista de [videos](https://www.youtube.com/playlist?list=PLUJnp-JI9H_xt-sOpr6hHTrrAgzsyp_H4) introductorios a la temática. Esto fue complementándose con otras [fuentes]().

Una vez comprendido el flujo básico de funcionamiento de estos modelos aplicados a un caso de estudio particular, se procedió a la planificación de las etapas del proyecto, alcance del mismo y distribución de las tareas. Las metodologías y adopciones de trabajo definidas para este proyecto se explican en este [link]().

Se realizaron pruebas tanto en local como en Colab utilizando distintas versiones del modelo LlaMa 2, teniendo en cuenta las limitaciones de procesamiento que fueron surgiendo a medida que se adicionaba mayor volumen de datos. El detalle de las diferentes versiones utilizadas así como su fundamentación se puede encontrar descripta en este [link](https://github.com/GoUpCloud/LLM2-db-documental/blob/development/docs/llm_doc.md).

### Demo del Modelo en Streamlit

Como framework de testing para el primer ChatBot sobre documentos se seleccionó [Streamlit](https://streamlit.io/), dado que es un framework muy popular para realizar aplicaciones web de manera fácil y rápida. Además cuenta con un módulo específico para aplicaciones de [Generative AI](https://streamlit.io/generative-ai) facilitando aún mas la creación de aplicaciones personalizadas utilizando modelos de generación de texto.

En primer lugar se desarrolló la aplicación en local, sin embargo los tiempos de respuesta fueron bajos y sin GPU disponible no se lograban resultados en tiempos aceptables. Por este motivo, se desarrolló una Notebook en Colab Pro donde fue posible el despliegue y utilización de la aplicación, consiguiendo la carga de varios documentos así como la conversación sobre ellos.

En este [link](https://github.com/GoUpCloud/LLM2-db-documental/tree/development/streamlit_app) se presenta todo el desarrollo realizado para el despliegue en local y en este [link](https://github.com/GoUpCloud/LLM2-db-documental/tree/development/streamlit_app_colab) se encuentra el desarrollo para el despliegue desde Colab Pro.

### Integración con DJango

Como framework para el MVP se eligio [Django](https://www.djangoproject.com/)  es un framework web Python de alto nivel que fomenta el desarrollo rápido y el diseño limpio, además de que su amplia variedad de funcionalidades preconstruidas agiliza el proceso de desarrollo y garantiza la escalabilidad del proyecto. Con las herramientas que tiene por defecto se implementó una funcionalidad de acceso a la aplicación mediante las opciones de *Login* y *Register*, con el objetivo de reforzar la seguridad y restringir el acceso no autorizado, considerando su posible evolución hacia un producto final en el futuro. 

El desarrollo comprendió la creación de dos páginas principales: una dedicada a la interacción con el modelo denominada "Chat", que incluye un historial de conversaciones y la interfaz principal para interactuar con el modelo, así como una página destinada a la carga de documentos.

La estructura de carpetas del proyecto Django incluye diversos elementos. La carpeta principal del proyecto lleva por nombre *djangochat* y alberga los documentos esenciales para la creación de una página web. Entre estos documentos se encuentran un archivo con instrucciones de inicio, otro que contiene las URL responsables de gestionar los endpoints de toda la aplicación, así como los archivos `asgi.py` y `wsgi.py`, utilizados por la página para manejar las directrices del servidor. También se encuentra un documento destinado a almacenar la memoria caché, con el propósito de agilizar la carga, y finalmente, las preferencias y ajustes del proyecto.

Paralelamente, se buscaron alternativas para el almacenamiento de los embeddings que se generan de los documentos, los cuales ocupaban espacio de disco y/o memoria si se utilizaban las base de datos vectoriales OpenSource. Por este motivo, y a modo de avanzar en los testeo de las distintas funcionalidades del proyecto, se optó por almacenar los embeddings en una base de datos vectorial llamada **Pinecone**, la cuál proporciona una capa gratuita para este tipo de proyectos de investigación. Toda la información detallada de su implementación se encuentra en este [link](https://github.com/GoUpCloud/LLM2-db-documental/tree/development/pinecone_colab).

Así mismo, se avanzó en algunas funcionalidades nuevas para el ChatBot, como integración de metadata para el control de carga de documentos y filtro de documentos a utilizar en la respuesta, búsqueda semántica por similitud del coseno y traducción de la respuesta al español.

### Azure

Se escogió el Azure container Registry (ACR) principalmente para controlar el almacenamiento de la imagen de la aplicación, este servicio permite compilar, almacenar y administrar imágenes y artefactos de contenedor en un registro privado para todo tipo de implementación de contenedor. El uso de ACR tiene como beneficio facilitar la implementación y administración de aplicaciones en contenedores, se integra facilmente con los servicios de Azure e incluye el contro de acceso y seguridad.

Al contar con la imagen en el contenedor se requirió un servicio de Azure que sirva para hospedar la aplicación web y se eligió Azure App Services (o solo Web Apps) que agrega a la aplicación la funcionalidad de Microsoft Azure, la seguridad, el equilibrio de carga el escalado automático y la administración automatizada.

## Contenido del repositorio

Este repositorio se organiza de la siguiente manera:

*    **core/**: es una carpeta de DJango donde se encuentra los archivos necesarios para la ejecución de la aplicación.
*    **djangochat/**: es una carpeta de DJango que contiene los documentos esenciales para la creación de una página web
*    **docs/**: es una carpeta que contiene la documentación detallada del proyecto de investigación
*    **pinecone_colab/**: es una carpeta que explica la implementación de Pinecone y nuevas funcionalidades para el Chat.
*    **manage.py**: es el archivo que se utiliza para ejecutar la aplciación de Django.
*    **requirements.txt**: son los requerimientos necesarios para ejecutar DJango.

## Recomendaciones

Para continuar con la investigación y desarrollo de la aplicación se recomenda tener en cuenta los siguientes puntos:

*    Definir el tipo de documentos que se podrán cargar. Esto es necesario para definir las técnicas de trozado de los documentos a partir de los cuales se realizan los embedding, los cuales al final generan el contexto necesario para generar la respuesta a una pregunta.
*    Investigar cómo mejorar el rendimiento en la lectura de documentos que contienen imágenes y tablas.
*    Experimentar con otros modelos de generación de los embedding.
*    Experimentar adicionando un prompt personalizado para mejorar la respuesta.
*    Experimentar adicionando un agente conversacional para mejorar la respuesta.

## Colaboradores del proyecto

El equipo de desarrollo de este proyecto consta de los siguientes participantes y roles:

Nombre	| Rol | Contacto
--- | --- | --- 
**Carla Pezzone**	| LLM DevOps | [![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)](https://github.com/IngCarlaPezzone) [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ingambcarlapezzone/)
**Jerson Carbajal**	| DB / Azure DevOps | [![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)](https://github.com/carbajaljerson) [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/jerson-carbajal-ramirez/)
**Jeremías Pombo**	| LLM DevOps / Knwoledge Base | [![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)](https://github.com/Jeremias44) [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/jeremiaspombo/)
**René Joo**	| DJango Developer / FullStack | [![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)](https://github.com/ReneSebastianJoo) [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ren%C3%A9-sebastian-joo-cisneros-65688914a/)
**David Echajaya**	| Project Manager / LLM DevOps |[![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)](https://github.com/Slindex) [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/david-echajaya/)

Cada uno de los roles se designaron tomando en consideración un balance entre las necesidades del proyecto, preferencias personales, habilidades y background de cada uno de los participantes.
