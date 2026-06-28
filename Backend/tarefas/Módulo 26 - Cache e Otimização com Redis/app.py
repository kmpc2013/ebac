# ---------------------------------------------------------------------------
# Importações
# ---------------------------------------------------------------------------
import asyncio
import random
import redis.asyncio as redis
import os
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
# modelo completo do livro (com id) — é o que fica salvo na lista
class LivrosDB(BaseModel):
    id_livro: int
    nome_livro: str
    autor_livro: str
    ano_livro: int


# dados que vem no body do POST/PUT (sem id, o id vem da URL ou é gerado)
class LivroUpdate(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


Livros_DB: list[LivrosDB] = []

# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------
app = FastAPI(
    title="API de livros",
    description="API para gerenciar catálogo de livros",
    version="1.0.0",
    contact={"name": "Luis Fernandes", "email": "luis.fernandes@sercompe.com.br"},
)


# simula operação lenta (tipo consulta no banco)
# o await libera o servidor enquanto espera, em vez de travar tudo
async def simular_delay():
    await asyncio.sleep(random.uniform(0, 1))


# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_TTL = int(os.getenv("REDIS_TTL", 60))

def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )


redis_client = get_redis_client()


async def salvar_livros_redis(livros: list[LivrosDB]):
    livros_json = [livro.dict() for livro in livros]
    await redis_client.set("livros", json.dumps(livros_json), ex=REDIS_TTL)

async def deletar_livros_redis():
    await redis_client.delete("livros")


@app.get("/livros/redis", status_code=200)
async def get_livros_redis():
    valor = await redis_client.get("livros")
    ttl = await redis_client.ttl("livros")
    if not valor:
        return {
            "chave": "livros",
            "ttl": ttl,
            "dados": [],
            "cache": "miss"
        }
    return {
        "chave": "livros",
        "ttl": ttl,
        "dados": json.loads(valor),
        "cache": "hit"
    }


# ---------------------------------------------------------------------------
# Rotas — saúde
# ---------------------------------------------------------------------------


@app.get("/")
async def hellow_world():
    return {"Hello": "World!"}


# ---------------------------------------------------------------------------
# Rotas — livros (CRUD)
# ---------------------------------------------------------------------------


# GET — lista todos os livros (async def + await no delay simulado)
@app.get("/livros", status_code=200)
async def get_livros():
    livros_cache = await redis_client.get("livros")
    if livros_cache:
        return json.loads(livros_cache)
    await simular_delay()
    await salvar_livros_redis(Livros_DB)
    return Livros_DB


# POST — cria livro, gera id automaticamente; 409 se o nome já existir
@app.post("/livros", status_code=201)
async def post_livros(livro: LivroUpdate):
    await simular_delay()
    Livros_nomes = [l.nome_livro for l in Livros_DB]
    if livro.nome_livro in Livros_nomes:
        raise HTTPException(status_code=409, detail="Livro já existe")

    novo_id = max((l.id_livro for l in Livros_DB), default=0) + 1
    novo_livro = LivrosDB(
        id_livro=novo_id,
        nome_livro=livro.nome_livro,
        autor_livro=livro.autor_livro,
        ano_livro=livro.ano_livro,
    )
    await deletar_livros_redis()
    Livros_DB.append(novo_livro)
    return {"message": "Livro adicionado com sucesso"}


# PUT — atualiza livro pelo id; 404 se não achar
@app.put("/livros/{id_livro}", status_code=200)
async def put_livros(id_livro: int, livro: LivroUpdate):
    await simular_delay()
    for livro_db in Livros_DB:
        if livro_db.id_livro == id_livro:
            livro_db.nome_livro = livro.nome_livro
            livro_db.autor_livro = livro.autor_livro
            livro_db.ano_livro = livro.ano_livro
            await deletar_livros_redis()
            return {"message": "Livro atualizado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não existe")


# DELETE — remove livro pelo id; 404 se não achar
@app.delete("/livros/{id_livro}", status_code=200)
async def delete_livros(id_livro: int):
    await simular_delay()
    for livro_db in Livros_DB:
        if livro_db.id_livro == id_livro:
            await deletar_livros_redis()
            Livros_DB.remove(livro_db)
            return {"message": "Livro deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não existe")
