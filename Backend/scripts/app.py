from fastapi import FastAPI, HTTPException

app = FastAPI()
tarefas = []


@app.get("/tarefa")
def get_tarefa():
    if not tarefas:
        raise HTTPException(status_code=400, detail="Nenhuma tarefa cadastrada")
    return tarefas

@app.post("/tarefa")
def post_tarefa(nome: str, desc: str):
    if any(t["nome"] == nome for t in tarefas):
        raise HTTPException(status_code=404, detail="Tarefa já existe")
    tarefas.append({"nome": nome, "descricao": desc, "concluida": False})
    return {"message": "Tarefa '{}' criada com sucesso".format(nome)}

@app.put("/tarefa")
def put_tarefa(nome: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome:
            tarefa["concluida"] = True
            return {"message": "Tarefa '{}' concluida!".format(nome)} 
    raise HTTPException(status_code=404, detail="Tarefa não existe")


@app.delete("/tarefa")
def delete_tarefa(nome: str):
    for i, tarefa in enumerate(tarefas):
        if tarefa["nome"] == nome:
            del tarefas[i]
            return {"message": "Tarefa '{}' removida!".format(nome)}
    raise HTTPException(status_code=404, detail="Tarefa não existe")