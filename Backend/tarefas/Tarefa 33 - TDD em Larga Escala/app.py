import os
import secrets

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

load_dotenv()
MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")


# ---------------------------------------------------------------------------
# Dependências
# ---------------------------------------------------------------------------

security = HTTPBasic()
def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )


# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API de livros",
    description="API para gerenciar catálogo de livros",
    version="1.0.0",
    contact={"name": "Luis Fernandes", "email": "luis.fernandes@sercompe.com.br"},
)

# ---------------------------------------------------------------------------
# Rotas — saúde
# ---------------------------------------------------------------------------


@app.get("/")
async def hellow_world(credentials: HTTPBasicCredentials = Depends(autenticar)):
    return {"Hello": "World!"}


# ---------------------------------------------------------------------------
# Rotas — livros (CRUD)
# ---------------------------------------------------------------------------


@app.post("/soma")
def calc_sum(a=int, b=int, credentials: HTTPBasicCredentials = Depends(autenticar)):
    try:
        result = int(a) + int(b)
    except Exception as a:
        raise HTTPException(status_code=400, detail="Valores inválidos.")
    return result

@app.post("/subtrair")
def calc_sub(a=int, b=int, credentials: HTTPBasicCredentials = Depends(autenticar)):
    try:
        result = int(a) - int(b)
    except Exception as a:
        raise HTTPException(status_code=400, detail="Valores inválidos.")
    return result

@app.post("/dividir")
def calc_div(a=int, b=int, credentials: HTTPBasicCredentials = Depends(autenticar)):
    try:
        result = int(a) / int(b)
    except Exception as a:
        raise HTTPException(status_code=400, detail="Valores inválidos.")
    return result

@app.post("/multiplicar")
def calc_mult(a=int, b=int, credentials: HTTPBasicCredentials = Depends(autenticar)):
    try:
        result = int(a) * int(b)
    except Exception as a:
        raise HTTPException(status_code=400, detail="Valores inválidos.")
    return result
