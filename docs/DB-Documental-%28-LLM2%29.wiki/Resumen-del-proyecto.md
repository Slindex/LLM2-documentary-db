# Introducción
---
Los **Large Language Models** (LLMs) son modelos de inteligencia artificial diseñados para comprender y generar texto haciendo uso del **Natural Language Processing** (NLP), en español, Procesamiento del Lenguaje Natural. Los LLM pueden generar texto coherente y relevante, responder preguntas y realizar tareas basadas en el lenguaje, lo cual los dota de capacidades increíbles para abordar y solucionar múltiples problemáticas relacionadas a la interpretación y generación del lenguaje.

Una problemática presente en la actualidad es la alta dificultad existente al momento de consultar grandes bases de datos documentales, especialmente cuando la información requerida se encuentra segmentada en múltiples documentos. Mediante la implementación y el uso de los LLMs es posible desarrollar agentes basados en IA capaces de responder a una consulta hecha por un usuario utilizando diversas fuentes de información como referencia.

Este proyecto busca utilizar **Llama2**, el LLM OpenSource más grande desarrollado hasta la fecha, con el fin de desarrollar una aplicación capaz de interpretar el contenido de múltiples archivos alojados en una base de datos documental. El contenido de estos archivos podrá ser consultado, accedido y resumido mediante el uso del **lenguaje natural** y contará con extensiones que almacenen texto **(.pdf, .txt, .md, etc...)**. Además, esta aplicación podrá responder consultas complejas que requieran acceder a la información de múltiples documentos.

Este proyecto se estructura de acuerdo con la siguiente **tabla de contenido**:

[[_TOC_]]

# Alcance del Proyecto
---
En esta sección se especifican las **acciones** a desempeñar, así como las **funcionalidades y aplicaciones** a desarrollar que se encuentran **dentro y fuera del campo de acción de este proyecto**. También se hace alusión a las **responsabilidades que asume este proyecto y sus implicados** en cuanto al uso de las aplicaciones o herramientas que se desarrollen en el mismo.
## Dentro del Campo de Acción
El campo de acción de este proyecto contempla la creación, desarrollo y configuración de un Producto Mínimo Viable (MVP) o Prototipo de un servicio web que use Llama2 como modelo de IA pre-entrenado para realizar consultas inteligentes a una base de datos documental. Este proyecto integra múltiples tecnologías **Open Source** de libre uso comercial, así como otras de libre uso personal para la creación de este MVP. Este proyecto contempla además la elaboración de documentación referente al funcionamiento del mismo, así como un video demostrativo en el que se detalla su uso en la práctica.

A continuación se enlistan algunos términos que se contemplan dentro del campo de acción de este proyecto:
* Producto Mínimo Viable
* Prototipo
* Testing de tecnologías
* Proyecto de investigación
* Fase Alpha de desarrollo
## Fuera del Campo de Acción
Bajo ninguna circunstancia este proyecto pretende desarrollar una aplicación final o comercial que pueda ser utilizada por el usuario común. La implementación de pruebas técnicas y de compatibilidad para el uso comercial o personal, así como la redacción de una guía de uso responsable están fuera del alcance de este proyecto. Por lo tanto, el usuario asume la responsabilidad de cualquier daño o perdida en la información que se produzca debido al uso del MVP desarrollado. El usuario también asume la responsabilidad del uso indebido que este le dé al MVP para otros fines.
# Desarrollo del Proyecto
---
## Contexto
Este proyecto se desarrolla como una pasantía empresarial para la empresa **Go Up Cloud** y, a su vez, como proyecto grupal de grado para el Bootcamp **Soy Henry**. Por lo tanto, la construcción de la aplicación propuesta dentro de los lineamientos y alcances del proyecto tendrá principalmente fines de investigación y desarrollo de productos basados en LLMs con potencial de derivar en una solución comercial que pueda ser desarrollada y utilizada a criterio, conveniencia y disposición por la empresa **Go Up Cloud**. El desarrollo de este proyecto se planea en el intervalo de tiempo de 1 mes:
* Desde: 25/Septiembre/2023
* Hasta: 20/Octubre/2023
## Etapas de Desarrollo
Este proyecto consta de 4 grandes etapas de desarrollo, cada una pensada para añadir funcionalidades al modelo de forma incremental. A continuación se enlistan:
* Desarrollo e Implementación del LLM
* Demo del Modelo en Streamlit
* Integración con DJango
* Integración de la DB

Cada una de las etapas de desarrollo del MVP son presentadas al CEO y gestora de proyectos de la empresa en el transcurso de 4 Sprints definidos de la siguiente forma:
## Equipo de Desarrollo
El equipo de desarrollo de este proyecto consta de los siguientes participantes y roles:

| Nombre         | Rol                          |
| -------------- | ---------------------------- |
| Carla Pezzone  | LLM DevOps                   |
| Jerson Carbajal| DB / Azure DevOps            |
| Jeremías Pombo | LLM DevOps / Knwoledge Base  |
| René Joo       | DJango Developer / FullStack |
| David Echajaya | Project Manager / LLM DevOps |

Cada uno de los roles se designaron tomando en consideración un balance entre las necesidades del proyecto, preferencias personales, habilidades y background de cada uno de los participantes.
## Directorio del proyecto

- **core**
    - **migrations**
        - 0001_initial.py
        - ´__init__´.py
    - **templates**
        - CargaDocumental.html
        - base.html
        - chat.html
        - frontpage.html
        - login.html
        - signup.html
    - ´__init__´.py
    - amdin.py
    - apps.py
    - forms.py
    - models.py
    - tests.py
    - urls.py
    - views.py
- **djangochat**
    - ´__init__´.py
    - asgi.py
    - settings.py
    - urls.py
    - wsgi.py
- .gitignore
- README.md
- manage.py
- requirements.txt

# Flujo de Trabajo
---
El flujo de trabajo del proyecto consta de 3 grandes corrientes: <span style="color: #3ba159;">Procesamiento de Documentos</span>, <span style="color: #2c4883;">Interpretación del LLM</span>, <span style="color: #6a5598;">Consulta del Usuario</span>. En el diagrama que se presenta a continuación se representa cada una de las corrientes mediante su respectivo color.

![Diagrama de Trabajo.png](/.attachments/Diagrama%20de%20Trabajo-2b166468-8e68-499d-876c-321a9f018b74.png)

# Convenciones y adopciones
---
## Siglas

- PR: Pull Request

## Idioma

- T**odo en el código, incluyendo clases, variables, constantes en inglés**
- Readme y notebooks **español**

Inglés para:

- Commits
- DocStrings
- Branches
- Código
- Pull Requests
- Comentarios

## Seguimiento del Proyecto

**GitHub** proyect para seguimiento del proyecto

**Notion** para compartir infromación

## Escritura de Commits y Branches

- **Commits** con formato conventional commit
- **No alterar** el mensaje de commit de los merge, dejar el que se genera automáticamente
- Branches informar sobre qué sección se trabaja y qué tipo de branch es: “feat/user_creation”
- **Main branch debe ser estable**. Para mergear hacia master/main hay que estar suficientemente confiado de que va a andar todo y no va a haber regresiones (romperse cosas que ya andaban)

### Estructura

```
<tipo>: <descripción>
<BLANK LINE>
[cuerpo opcional]
<BLANK LINE>
[nota(s) al pie opcional(es)]

Ejemplo: 

"refactor: Modified addUsers() for testing performance

In users.py lines 23 - 30 were changed

Resolve: #11"
```

- En **<tipo>** se puede poner:
    - **fix**: corrige un error en la base del código
    - **feat**: introduce una nueva funcionalidad en la base del código
    - **style:** cambios que no afectan al significado del código (espacios en blanco, formato, falta de punto y coma, etc.)
    - **refactor:** refactorizacion del código en producción.
    - **docs**: solo cambio la documentación
- En **<descripción>**:
    - no debe contener mas de 50 caracteres
    - debe iniciar con una letra mayúscula
    - no terminar con un punto
    - hay que ser objetivos y muy importante
- En **[cuerpo opcional]**:
    - es opcional
    - se usan en caso de que el commit requiera una explicación y contexto
- En **[nota(s) al pie opcional(es)]**:
    - es opcional
    - es usado para el seguimiento de los IDs con incidencias. Por ejemplo: resuelve: #5 (issue número 5)
- En **funciones**:
    - Escribir con doble paréntesis al final: ()

## Escritura de Pull Requests

- Un PR debe comunicar en qué consiste el cambio y por qué es necesario.
    - **Título**: poner "**WIP:** " si se hace el PR antes que este listo para revisión. Sino tiene que ser claro sobre qué esta cambiando
    - **Descripción**: debe indicar el por qué y el cómo del cambio y qué se cambió o agregó.
    - **Revisor**: etiquetar a la persona revisora
    - **Commits**: ayudan al revisor a entender los cambios
- Revisores:
    - Tener en cuenta el contexto indicado por el autor.
    - Proporcione comentarios constructivos.
    - Recuerda comentar las cosas buenas.
- Autores:
    - Aplique los cambios debidos a los comentarios de los revisores como commits adicionales, y subir una vez que el PR esté listo para fusionar.

## Convención del Código
### Nombrado

- **Variables y funciones**: camelCase
- **Constantes**: FILE_PATH
- **Clases**: UnaClase

⚠️ *Usar el nombre justo implica que el nombre de la variable permita entender específicamente qué contiene dicha variable a cualquiera que esté mínimamente familiarizado con el código del proyecto*

### Docstring

```
'''
Guarda la calificación asociada a un texto en la base de datos.

Parameters:
texto (str): El texto al que se le asignará la calificación.
calificacion (int): La calificación a asignar al texto.

Returns:
None
'''
```

### Comentarios

- El código tiene que poder entenderse lo máximo posible sin comentarios
- Si todavía vemos beneficioso dejar un comentario, que sea claro y directo y esté bien cerca de lo que aclara.

## Code review

- Avisar al **reviewer** cuando un PR está listo para revisar.
- Si el PR se crea antes de estar listo poner al principio del título "**WIP:** ", y sacarlo cuando el PR se considere feature-complete, testeado y estable.
- Hacer **refactors** y **clean-ups** antes de considerar un PR como listo.
    - *Refactors* significa reestructurar el código fuente, alterando la estructura interna sin cambiar su comportamiento externo.
    - *Clean-ups* significa limpiar de códigos comentados que no se usan, acomodar, etc.
- Una vez que está aprobado, se recomienda que el **autor del PR sea quien lo mergee**.

⚠️ *El code review no supone entender hasta el último detalle cada línea de código ajena pero, sí incentiva a que tengamos una visión global del proyecto; queremos tener una idea clara de las partes que lo componen y cómo se relacionan.*

## Workflow en Github

1. **Clonar** el repo forkeado.
2. **Crear** la rama del **Issue**
3. **Ubicar** la rama correspondiente al **Issue** en el que se está trabajando.
4. Trabajar en local y commitiar cambios. Una vez llegada a la versión final de lo que estés trabajando **pushear** los cambios al repo forkeado.
5. Hacer un **PR** a la rama **Development** solicitando a un revisor la revisión.
6. Con la aprobación de tu revisor se puede **mergear.**
7. En cada **Daily**, si se considera posible **mergear** a la **Main**, se mergea.