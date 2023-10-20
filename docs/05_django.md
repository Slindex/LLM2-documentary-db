# Documentación de Django

Este apartado esta hecho para que todos los miembros puedan generar en local el proyecto en Django, puedan instalar los requerimientos necesarios y probarlo.

## Inicialización 

Para empezar se arma un entorno virtual con la finalidad de tener un mejor control de las dependencias y el proyecto pueda ser dockerizado a futuro.

Una vez creado el entorno virtual bajamos en el Django.

~~~
pip install django
pip install dotenv
~~~

Se instala dotenv para poder hacer el manejo de los datos sensibles como las contraseñas y tokens. 

Una vez instalado procedemos a general la aplicación con 

~~~
python manage.py startapp 
~~~

Se crea el proyecto

## Creacion de endpoints

Al trabajar con el modelo MVC (Model, Vista, Controlador), vamos a generar cada endpoint colocando un template(vista), que debe refenciarse en urls.py y en views.py( controlador).add()

## Creacion de templates

Para hacer un template hay que crear un documento html que contenga la información necesaria, de ahi cargar el template base.html

## Creacion de una funcionalidad

Para hacer una nueva funcion hay que ir a **views.py** y ahi hacer la funcion, si esta requiere que la persona este autenticada se coloca el decorador **@login_required** arriba de la funcion. Se debe tomar en cuenta que se requiere retornar como ***return render(request, 'core/pagina.html')***. 

Ejemplo de función:

~~~
def frontpage (request):
    return render(request, 'core/frontpage.html')
~~~

# La carpeta Core

El proyecto de Django incluye la Carpeta Core que es la carpeta en donde vive nuestro proyecto y lo que la da las funcionalidades. 

Tiene una estructura de carpetas, en las que se encuentran.

- __pycache__
- migrations
- templates/core

###  __pycache__

En **pycache** tenemos cache de nuestro proyecto es una carpeta autogenerada y no debe ser tocada.add()

### migrations
Contiene información de la base de datos por defecto de Django que es SQLite3, en ella estan los modelos de registro así como los de las query

### templates/core

En **templates** se deben colocar todos los archivos estaticos, los cuales son paginas html, css y javascript que nos ayudaran a visualizar la información. Tiene la carpeta core para tener aqui todas las paginas requeridas para las vistas de core y si el proyecto crece se añadan nuevas paginas para esas funcionalidades.

## Archivos dentro de core

Se tienen ademas archivos dentro de core que son los siguientes:

-  ´__init.py__´
-  .env
-  admin.py 
- apps.py 
- * **forms.py**
- * **models.py**
- test.py 
- * **urls.py**
- * **views.py**

De los anteriores solo se modifican los que estan en negritas. 

### .env

Es el archivo donde se guardan contraseñas o claves de token para que sean mas seguras ya que el archivo .gitignore no sube esto.

### forms.py 

aqui se tienen los forms que se utilizan en la aplicacón tanto el de signup como el utilizado para subir documentos. 

### models.py 

Aqui se encuentran los modelos, que son clases para que se utilizan cuando la aplicacion las requiera. 

#### create_slugg

Este modelo genera un slgu utilizado por la Userquery para su funcionamiento

#### Userquery

Es el modelo que guarda las **query** de los usuarios, para que aparezcan en el chat

## urls.py 

Aqui se encuentran las direcciones de cada pagina, esta se debe referenciar en la función urlpaterns. 

En la funcion se nos pide un path que es el endpoint solicitado, dentro del cual tenemos que:

-colocar la direcion entre comillas y una barra final, *ejemplo: **'signup/'*** 
- La pagina a la que vamos desde views *ejemplo: views.chat,* 
- El nombre del endpoint con la sentencia **name=** y el nombre entre comillas *ejemplo name='frontpage'*

## views.py 

Este es el cerebro de la aplicación, aqui se encuentran las funciones, aqui se llama a langchain y cualquier libreria requerida para darle más funcionalidades.

Consta de dos grandes partes, la primera donde se llaman a las librerias y la segunda donde se declaran las funciones. 

### Librerias

Este espacio se separa en dos categorias tambien las importaciones de Django y las de langchain



Las funciones son las siguientes:
- 

### frontpage

Funcion que hace la pagina principal

### signup

Funcion que genera la forma de registro, ademas de colocar dentro de la DB a los usuarios nuevos

### chat

La funcion principal que nos genera la pagina del chat permite el input por parte de los usuarios y el output del modelo

### CargaDocumental

La funcion que nos da la pagina para cargar documentos y su gestión

### AI_GGML

Esta es la primer funcion que no genera una pagina nueva sino utiliza la pagina de chat y retorna en ella.

Esta funcion carga el modelo, permite que las queries del usuario sean ingestadas al modelo.

