# HACKYAgentes

## Descripción

HACKYAgentes es una aplicación desarrollada con FastAPI que permite la creación y gestión de proyectos y aprendices mediante agentes inteligentes.

## Requisitos

- Python 3.8 o superior
- FastAPI
- Pydantic
- Requests
- python-dotenv

## Instalación

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/HarbyT/HACKYAgentes.git

Navega al directorio del proyecto:

## bash
cd HACKYAgentes
Crea y activa un entorno virtual (opcional pero recomendado):

## bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instala las dependencias:

## bash
pip install -r requirements.txt
Configuración
## Crea un archivo .env en la raíz del proyecto con la siguiente variable:

OPENAI_API_KEY=tu_clave_de_api
Reemplaza tu_clave_de_api con tu clave de API de OpenAI.

## Ejecución
Inicia la aplicación con el siguiente comando:

uvicorn main:app --reload
La aplicación estará disponible en http://127.0.0.1:8000.

## Uso
Crear un proyecto: Envía una solicitud POST a /create_project/ con los datos del proyecto.
Añadir un aprendiz: Envía una solicitud POST a /add_learner/ con los datos del aprendiz.
Crear un proyecto aleatorio: Envía una solicitud POST a /create_random_project/.
Para más detalles, consulta la documentación interactiva en http://127.0.0.1:8000/docs.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.