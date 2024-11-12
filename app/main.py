from fastapi import FastAPI
from .database import create_indexes
from .routes import router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Crear los índices al iniciar la aplicación
    await create_indexes()

app.include_router(router)
