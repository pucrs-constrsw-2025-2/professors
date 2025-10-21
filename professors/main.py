from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio  # <--- 1. Import asyncio

# Importações absolutas a partir do pacote 'professors'
from professors.config import get_settings
from professors.adapters.api.routes import classes, courses, lessons, professors
from professors.adapters.database.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando serviço Professors...")
    print(f"Conectando ao DB: {get_settings().DATABASE_URL.split('@')[-1]}")
    
    print("Verificando e criando tabelas (se não existirem)...")
    try:
        await asyncio.to_thread(Base.metadata.create_all, bind=engine)
        print("Tabelas prontas.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    
    yield
    print("Encerrando serviço Professors...")

app = FastAPI(
    title="Professors Microservice",
    description="API para gerenciamento de professores",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(professors.router)
app.include_router(classes.router)
app.include_router(courses.router)
app.include_router(lessons.router)

@app.get("/", tags=["Health Check"], summary="Verifica a saúde da API")
def read_root():
    return {"status": "ok"}