from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="API Estacionamiento", lifespan=lifespan)

# — Aquí pega el ping —
@app.get("/ping")
async def ping():
    return {"pong": "pong"}

# Importa routers *después* de crear `app`
from routers.entrada import router as entrada_router
from routers.cobro   import router as cobro_router

app.include_router(entrada_router, prefix="/api/entrada", tags=["Entrada"])
app.include_router(cobro_router,   prefix="/api/cobro",   tags=["Cobro"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}


