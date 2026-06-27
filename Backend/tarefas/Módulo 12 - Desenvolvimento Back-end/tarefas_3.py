from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets


# Classes
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Configuração da API
app = FastAPI(
    title="API de tarefas",
    description="API para gerenciar tarefas",
    version="3.0.0",
    contact={
        "name": "Luis Fernandes",
        "email": "luis.fernandes@sercompe.com.br"
    }
)
tarefas_db: list[Tarefa] = []
MEU_USUARIO = "admin"
MINHA_SENHA = "admin"
security = HTTPBasic()

# Funções
def validar_credenciais(usuario: str, senha: str) -> bool:
    usuario_correto = secrets.compare_digest(usuario, MEU_USUARIO)
    senha_correta = secrets.compare_digest(senha, MINHA_SENHA)
    return usuario_correto and senha_correta


def autenticar(credentials: HTTPBasicCredentials = Depends(security)) -> HTTPBasicCredentials:
    if not validar_credenciais(credentials.username, credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials

@app.get("/tarefa")
def get_tarefa(page: int = 1, size: int = 3, order: str = "nome", credentials: HTTPBasicCredentials = Depends(autenticar)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page ou size estão com valores inválidos.")
    if not tarefas_db:
        return {"message": "Nenhuma tarefa adicionada"}
    
    if order == "nome":
        tarefas_ordenadas = sorted(tarefas_db, key=lambda x: x.nome)
    elif order == "descricao":
        tarefas_ordenadas = sorted(tarefas_db, key=lambda x: x.descricao)
    elif order == "concluida":
        tarefas_ordenadas = sorted(tarefas_db, key=lambda x: x.concluida)
    else:
        raise HTTPException(status_code=400, detail="Order inválido")

    start = (page - 1) * size
    end = start + size
    tarefas_paginadas = tarefas_ordenadas[start:end]

    return tarefas_paginadas

@app.post("/tarefa", status_code=201)
def post_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar)):
    if any(tarefa.nome == t.nome for t in tarefas_db):
        raise HTTPException(status_code=409, detail="Tarefa já existe")
    tarefas_db.append(tarefa)
    return {"message": "Tarefa '{}' criada!".format(tarefa.nome)}

@app.put("/tarefa", status_code=200)
def put_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar)):
    for t in tarefas_db:
        if t.nome == tarefa.nome:
            t.descricao = tarefa.descricao
            t.concluida = tarefa.concluida
            return {"message": "Tarefa '{}' atualizada!".format(tarefa.nome)} 
    raise HTTPException(status_code=404, detail="Tarefa não existe")


@app.delete("/tarefa", status_code=200)
def delete_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar)):
    for t in tarefas_db:
        if t.nome == tarefa.nome:
            tarefas_db.remove(t)
            return {"message": "Tarefa '{}' removida!".format(tarefa.nome)}
    raise HTTPException(status_code=404, detail="Tarefa não existe")