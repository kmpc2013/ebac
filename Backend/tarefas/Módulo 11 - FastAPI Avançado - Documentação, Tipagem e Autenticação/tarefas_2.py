from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

app = FastAPI()
tarefas_db: list[Tarefa] = []

@app.get("/tarefa")
def get_tarefa():
    if not tarefas_db:
        return {"message": "Nenhuma tarefa adicionada"}
    return tarefas_db

@app.post("/tarefa", status_code=201)
def post_tarefa(tarefa: Tarefa):
    if any(tarefa.nome == t.nome for t in tarefas_db):
        raise HTTPException(status_code=409, detail="Tarefa já existe")
    tarefas_db.append(tarefa)
    return {"message": "Tarefa '{}' criada!".format(tarefa.nome)}

@app.put("/tarefa", status_code=200)
def put_tarefa(tarefa: Tarefa):
    for t in tarefas_db:
        if t.nome == tarefa.nome:
            t.descricao = tarefa.descricao
            t.concluida = tarefa.concluida
            return {"message": "Tarefa '{}' atualizada!".format(tarefa.nome)} 
    raise HTTPException(status_code=404, detail="Tarefa não existe")


@app.delete("/tarefa", status_code=200)
def delete_tarefa(tarefa: Tarefa):
    for t in tarefas_db:
        if t.nome == tarefa.nome:
            tarefas_db.remove(t)
            return {"message": "Tarefa '{}' removida!".format(tarefa.nome)}
    raise HTTPException(status_code=404, detail="Tarefa não existe")