## Instalación de Docker en Linux

Ejecute el siguiente comando para desinstalar todos los paquetes conflictivos:

```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Antes de instalar Docker Engine por primera vez en una nueva máquina host, debe configurar el repositorio de Docker. Luego, puede instalar y actualizar Docker desde el repositorio.

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
Instale los paquetes de Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verifique que la instalación de Docker Engine sea exitosa ejecutando la imagen de hello-world.

```bash
sudo docker run hello-world
```

Este comando descarga una imagen de prueba y la ejecuta en un contenedor. Cuando el contenedor se ejecuta, imprime un mensaje de confirmación, de esta manera se ha instalado e iniciado Docker Engine con éxito.

## Acceso
Se debe tener las credenciales para acceder en [Azure](https://portal.azuree.com) así como en [Docker](https://hub.docker.com)

## Creación de Container Azure

Crear el container donde se publicará la imagen, para esto se debe ingresar un grupo, el nombre de registro, la ubicación y el SKU Standard 
<p align=center>
<img src="src\container.png" height = 560 weight=560>
<p>
Se continua con lo recomendado en la Configuración de Redes
<p align=center>
<img src="src\container2.png" height = 425 weight=525>
<p>
Se avanza hasta la pestaña Review para finalmente dar click en Crear
<p align=center>
<img src="src\container3.png" height = 400 weight=500>
<p>
Una vez completado el deployment se va al recurso
<p align=center>
<img src="src\container4.png" height = 500 weight=550>
<p>
Es aquí donde se guardará la imagen de Docker
<p align=center>
<img src="src\container5.png" height = 330 weight=330>
<p>
En el menú de la izquierda se selecciona Access Keys y se habilita el Usuario Administrador. 



## Creación del Docker File
Antes de generar la imagen se debe crear el archivo Docker de la Aplicación. La ubiación del archivo docker debe estar dentro de la aplicación.

```bash
# Use the official Python image
FROM python:3.11.4

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install required Python packages
RUN pip install -r requirements.txt --default-timeout=100 future

# Copy the rest of the application files to the container's working directory
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8000

# Command to run your Streamlit application
CMD python manage.py runserver
```
Estro nos servirá luego para la creación de la imagen base y posteriormente la imagen nos servirá para ejecutar la aplicación dentro de un container. 

## Creación de imagen de Docker desde Linux

Debemos ubicarnos en la carpeta de la aplicación y abrimos la consola

```bash
#list of images 
sudo docker images

#check containers
sudo docker ps

#create image where chatbotimg it's image's name
sudo docker build -t  chatbotimg .

#check image that was created
sudo docker images

#exec the image to verify it
sudo docker run chatbotimg 

```
## Creación Container Instances

Seleccionar Home y buscar Container Instances 
<p align=center>
<img src="src\container6.png" height = 290 weight=290>
<p>
Dar click en Crear Container Instances

