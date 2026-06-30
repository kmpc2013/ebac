from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import secrets

# Inicialização do banco de dados e da sessão
DATABASE_URL = "sqlite:///./tarefas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def sessao_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

class TarefaDB(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, index=True)
Base.metadata.create_all(bind=engine)

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

# CRUD
@app.get("/tarefa")
def get_tarefa(page: int = 1, size: int = 3, order: str = "nome", db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page ou size estão com valores inválidos.")  

    if order == "id":
        tarefas_db = db.query(TarefaDB).order_by(TarefaDB.id).offset((page - 1) * size).limit(size).all()
    elif order == "nome":
        tarefas_db = db.query(TarefaDB).order_by(TarefaDB.nome).offset((page - 1) * size).limit(size).all()
    elif order == "descricao":
        tarefas_db = db.query(TarefaDB).order_by(TarefaDB.descricao).offset((page - 1) * size).limit(size).all()
    elif order == "concluida":
        tarefas_db = db.query(TarefaDB).order_by(TarefaDB.concluida).offset((page - 1) * size).limit(size).all()
    else:
        raise HTTPException(status_code=400, detail="Order inválido")

    if not tarefas_db:
        return {"message": "Nenhuma tarefa adicionada"}

    return tarefas_db

@app.post("/tarefa", status_code=201)
def post_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome).first()
    if db_tarefa:
        raise HTTPException(status_code=409, detail="Tarefa já existe")
    nova_tarefa = TarefaDB(nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return {"message": "Tarefa '{}' criada!".format(tarefa.nome)}

@app.put("/tarefa", status_code=200)
def put_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não existe")
    db_tarefa.nome = tarefa.nome
    db_tarefa.descricao = tarefa.descricao
    db_tarefa.concluida = tarefa.concluida
    db.commit()
    db.refresh(db_tarefa)
    return {"message": "Tarefa '{}' atualizada!".format(tarefa.nome)}

@app.delete("/tarefa", status_code=200)
def delete_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não existe")
    db.delete(db_tarefa)
    db.commit()
    return {"message": "Tarefa '{}' removida!".format(tarefa.nome)}
