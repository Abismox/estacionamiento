
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización al arrancar la aplicación
    init_db()
    yield
    # Aquí podrías agregar tareas de limpieza si fueran necesarias

app = FastAPI(title="API Estacionamiento", lifespan=lifespan)
