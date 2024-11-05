from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List, Optional
import os
from swarm import Swarm, Agent
import random
import requests
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()

# Asignar la API Key desde el entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API Key en el archivo .env. Por favor asegúrate de que OPENAI_API_KEY esté correctamente configurada.")

os.environ["OPENAI_API_KEY"] = api_key

# Inicializamos FastAPI
app = FastAPI()

# Creamos el cliente de Swarm
client = Swarm()

# Definimos una base de datos simulada para almacenar los datos de proyectos, pasos, categorías, y aprendices.
project_database = {
    "projects": {},
    "categories": ["Web Development", "Data Science", "Machine Learning", "DevOps"],
    "learners": {},
    "skills": ["Python", "JavaScript", "Docker", "SQL", "Machine Learning"],
}

# Modelos para FastAPI
class ProjectModel(BaseModel):
    title: str
    short_description: str
    description: str
    submission_date: str
    delivery_date: str
    expiration_date: str
    development_time: str
    difficulty: str
    bounty: float
    urls: List[str]

class LearnerModel(BaseModel):
    person_id: str
    experience_level: str
    education: str
    biography: str
    interest: str
    country: str

# Definimos una función para crear proyectos
def create_project( title: str, short_description: str, description: str, submission_date: str, delivery_date: str, expiration_date: str, development_time: str, difficulty: str, bounty: float, urls: List[str]) -> str:
    
  
    """
    Crea un proyecto basado en la información proporcionada.
    """

    
    # Creamos un ID para el proyecto
    project_id = str(len(project_database["projects"]) + 1)
    
    # Creamos el proyecto
    project = {
        
        "title": title,
        "short_description": short_description,
        "description": description,
        "submission_date": submission_date,
        "delivery_date": delivery_date,
        "expiration_date": expiration_date,
        "status": "New",
        "development_time": development_time,
        "difficulty": difficulty,
        "bounty": bounty,
        "urls": urls,
    }
    
    # Guardamos el proyecto en la base de datos
    project_database["projects"][project_id] = project
    
    # Enviar proyecto a la API externa
    response = requests.post("https://asterion.casa/api/v1/projects", json=project)
    if response.status_code == 201:
        return f"Proyecto creado exitosamente con ID: {project_id} y enviado a la API externa."
    else:
        return f"Proyecto creado localmente con ID: {project_id}, pero ocurrió un error al enviarlo a la API externa: {response.status_code} - {response.text}"

# Definimos una función para agregar aprendices
def add_learner(person_id: str, experience_level: str, education: str, biography: str, interest: str, country: str) -> str:
    """
    Añade un aprendiz con la información proporcionada.
    """
    learner = {
        "person_id": person_id,
        "experience_level": experience_level,
        "education": education,
        "biography": biography,
        "interest": interest,
        "country": country,
    }
    project_database["learners"][person_id] = learner
    return f"Aprendiz {person_id} añadido con éxito."

# Función para crear un proyecto aleatorio
def create_random_project() -> str:
    """
    Crea un proyecto con datos aleatorios.
    """

    title = f"Proyecto Aleatorio segun lo aletoreo"
    short_description = "Este es un proyecto generado aleatoriamente."
    description = "Descripción detallada de un proyecto generado de forma aleatoria."
    submission_date = "2024-11-15"
    delivery_date = "2024-12-01"
    expiration_date = "2025-01-01"
    development_time = "2 semanas"
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    bounty = round(random.uniform(100.0, 1000.0), 2)
    urls = ["http://example.com/proyecto"]
    
    return create_project( title, short_description, description, submission_date, delivery_date, expiration_date, development_time, difficulty, bounty, urls)

# Endpoints CRUD para proyectos y aprendices
@app.post("/create_project/")
async def create_project_endpoint(project: ProjectModel):
    response = create_project(
        #product_owner_id=project.product_owner_id,
        #category_id=project.category_id,
        title=project.title,
        short_description=project.short_description,
        description=project.description,
        submission_date=project.submission_date,
        delivery_date=project.delivery_date,
        expiration_date=project.expiration_date,
        development_time=project.development_time,
        difficulty=project.difficulty,
        bounty=project.bounty,
        urls=project.urls
    )
    return {"message": response}

@app.post("/add_learner/")
async def add_learner_endpoint(learner: LearnerModel):
    response = add_learner(
        person_id=learner.person_id,
        experience_level=learner.experience_level,
        education=learner.education,
        biography=learner.biography,
        interest=learner.interest,
        country=learner.country
    )
    return {"message": response}

@app.post("/create_random_project/")
async def create_random_project_endpoint(project: ProjectModel):
    response = create_random_project(
        #product_owner_id=project.product_owner_id,
        #category_id=project.category_id,
        title=project.title,
        short_description=project.short_description,
        description=project.description,
        submission_date=project.submission_date,
        delivery_date=project.delivery_date,
        expiration_date=project.expiration_date,
        development_time=project.development_time,
        difficulty=project.difficulty,
        bounty=project.bounty,
        urls=project.urls)
    return {"message": response}

# Definimos un agente de creación de proyectos
project_creation_agent = Agent(
    name="Agente Creador de Proyectos",
    instructions="""
    Eres un agente que crea proyectos basados en los datos proporcionados por el usuario.
    Solicita la información necesaria al usuario para poder crear un proyecto, incluyendo título, descripción, fechas, categoría, nivel de dificultad y cualquier otro dato relevante.
    También puedes generar un proyecto aleatorio si el usuario lo solicita, y debes entregar el resultado en formato JSON para que pueda ser enviado a una API externa.
    Cuando veas que el proyecto es aleatorio completaras algunos campos requeridos, como `category_id` y `product_owner_id
    """,
    functions=[create_project, create_random_project]
)

# Definimos un agente para manejar aprendices y habilidades
learner_management_agent = Agent(
    name="Agente de Gestión de Aprendices",
    instructions="""
    Eres un agente que gestiona aprendices, añadiendo sus datos y asignando habilidades relevantes.
    Solicita la información completa del aprendiz, como nivel de experiencia, educación, intereses y país de origen.
    Usa la información proporcionada para almacenar y categorizar aprendices, y luego entrega el resultado en formato JSON.
    """,
    functions=[add_learner]
)

# Probamos el agente de creación de proyectos

messages = [
    {
        "role": "user",
        "content": "Quiero crear un proyecto aleatoreo'."
    }
]

response = client.run(agent=project_creation_agent, messages=messages)
print(response.messages[-1]["content"])

