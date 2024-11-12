# User Microservice with FastAPI and MongoDB

Este proyecto implementa un microservicio de usuarios usando FastAPI y MongoDB, todo ejecutado en contenedores Docker.

## Requisitos previos

1. Docker y Docker Compose instalados.
2. Python 3.8 o superior si deseas ejecutar el código localmente sin Docker.

## Configuración del entorno

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/FranciscoLopezKanto/user-microservice-FastApi
    cd user-microservice-FastAPI
    ```

2. Crear un archivo `.env` en el directorio raíz y configurar las variables de entorno. Ejemplo:

    ```env
    APP_NAME=API
    APP_HOST=0.0.0.0
    APP_PORT=8000
    MONGODB_URI=mongodb://admin:password@mongodb:27017
    MONGODB_DATABASE=user_database
    ```

3. Configurar Docker Compose y ejecutar el proyecto en contenedores.

## Uso

### Ejecutar en Docker

1. Construir y correr los contenedores de Docker:
    ```bash
    docker-compose up -d
    ```

2. Verificar los contenedores en ejecución:
    ```bash
    docker ps
    ```

3. Acceder a la API en `http://localhost:8000`.

### Comandos útiles de Docker

- Para ver los logs de un contenedor específico:
  ```bash
  docker logs nombre_del_contenedor
Para detener los contenedores:
bash
Copiar código
docker-compose down
Ejecutar localmente (sin Docker)
Si prefieres correr el proyecto localmente:

## Crear y activar un entorno virtual:

bash
Copiar código
python3 -m venv venv
source venv/bin/activate
Instalar las dependencias:

bash
Copiar código
pip install -r requirements.txt
Ejecutar el servicio de FastAPI:

bash
Copiar código
uvicorn app.main:app --reload
La API estará disponible en http://localhost:8000.

## Estructura del Proyecto
app/: Código de la aplicación.
app/main.py: Archivo principal donde se configura la aplicación FastAPI.
app/database.py: Configuración de la conexión con MongoDB.
Dockerfile: Configuración para el contenedor de la aplicación FastAPI.
docker-compose.yml: Configuración de Docker Compose.
## Notas adicionales
Asegúrate de que MongoDB esté configurado con autenticación en Docker. Si experimentas problemas de conexión, revisa los logs de MongoDB y el archivo .env.