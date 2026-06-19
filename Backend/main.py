import asyncio
import json
import os
import secrets
import redis

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from tasks import somar, fatorial
from celery_app import celery_app
from celery.result import AsyncResult
from kafka_producer import enviar_evento

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# ---------------------------------------------------------------------------
# Banco de dados
# ---------------------------------------------------------------------------

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer, index=True)


Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------

redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True,
)

def salvar_livro_redis(livro_id: int, livro: Livro):
    redis_client.set(f"livro:{livro_id}", json.dumps(livro.dict()))

def deletar_livro_redis(livro_id: int):
    redis_client.delete(f"livro:{livro_id}")

# ---------------------------------------------------------------------------
# Dependências
# ---------------------------------------------------------------------------

security = HTTPBasic()


def sessao_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )

# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API de livros",
    description="API para gerenciar catálogo de livros",
    version="1.0.0",
    contact={
        "name": "Luis Fernandes",
        "email": "luis.fernandes@sercompe.com.br"
    }

)

# ---------------------------------------------------------------------------
# Rotas — saúde
# ---------------------------------------------------------------------------

@app.get("/")
async def hellow_world():
    return {"Hello": "World!"}

# ---------------------------------------------------------------------------
# Rotas — celery
# ---------------------------------------------------------------------------

@app.post("/calcular/soma")
def calcular_soma(a: int, b: int):
    tarefa = somar.delay(a, b)
    redis_client.lpush("tarefas_ids", tarefa.id)
    redis_client.ltrim("tarefas_ids", 0, 49) 
    return {"task_id": tarefa.id, "message": "Tarefa de soma enviada para execução!"}

@app.post("/calcular/fatorial")
def calcular_fatorial(n: int):
    tarefa = fatorial.delay(n)
    redis_client.lpush("tarefas_ids", tarefa.id)
    redis_client.ltrim("tarefas_ids", 0, 49) 
    return {"task_id": tarefa.id, "message": "Tarefa de fatorial enviada para execução!"}

@app.get("/tarefas/recentes")
def listar_tarefas_recentes():
    tarefas_ids = redis_client.lrange("tarefas_ids", 0, 49)
    tarefas_info = []
    for task_id in tarefas_ids:
        resultado = AsyncResult(task_id, app=celery_app)
        tarefas_info.append({
            "task_id": task_id,
            "status": resultado.status,
            "result": resultado.result if resultado.successful() else None
        })
    return {"tarefas": tarefas_info}

# ---------------------------------------------------------------------------
# Rotas — livros (CRUD)
# ---------------------------------------------------------------------------

@app.get("/livros")
def get_livros(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar)
    ):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos.")
     
    cache_key = f"livros:page={page}:limit={limit}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()
    if not livros:
        return {"message": "Nenhum livro encontrado."}
    
    total_livros = db.query(LivroDB).count()
    resposta = {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [
            {
                "id": livro.id, 
                "nome_livro": livro.nome_livro, 
                "autor_livro": livro.autor_livro, 
                "ano_livro": livro.ano_livro
            } for livro in livros
        ]
    }
    redis_client.setex(cache_key, 30,  json.dumps(resposta))
    return resposta

@app.post("/adiciona")
async def post_livro(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Livro já existe.")
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    salvar_livro_redis(novo_livro.id, livro)
    enviar_evento("livros", {"action": "create", "data": livro.model_dump()})
    return {"message": "Livro adicionado!!"}

@app.put("/atualiza/{id_livro}")
async def put_livro(id_livro: int, livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro
    db.commit()
    db.refresh(db_livro)
    return {"message": "Livro atualizado!!"}

@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(db_livro)
    db.commit()
    deletar_livro_redis(id_livro)
    return {"message": "Livro deletado!!"}

# ---------------------------------------------------------------------------
# Rotas — demonstração
# ---------------------------------------------------------------------------

async def chamadas_externas_1():
    await asyncio.sleep(2)
    return "Resultado chamada externa 1"

async def chamadas_externas_2():
    await asyncio.sleep(2)
    return "Resultado chamada externa 2"

async def chamadas_externas_3():
    await asyncio.sleep(2)
    return "Resultado chamada externa 3"

@app.get("/chamadas-externas")
async def chamadas_externas():
    tarefa1 = asyncio.create_task(chamadas_externas_1())
    tarefa2 = asyncio.create_task(chamadas_externas_2())
    tarefa3 = asyncio.create_task(chamadas_externas_3())

    resultado1 = await tarefa1
    resultado2 = await tarefa2
    resultado3 = await tarefa3

    return {
        "mensagem": "Todas as chamadas nas API's foram concluidas com sucesso",
        "resultado": [resultado1, resultado2, resultado3]
    }

# ---------------------------------------------------------------------------
# Rotas — debug
# ---------------------------------------------------------------------------

@app.get("/debug/redis")
def ver_livros_redis():
    chaves = redis_client.keys("livros:*")
    livros = []
    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)
        livros.append({
            "chave": chave,
            "valor": json.loads(valor),
            "ttl": ttl
        })
    return livros