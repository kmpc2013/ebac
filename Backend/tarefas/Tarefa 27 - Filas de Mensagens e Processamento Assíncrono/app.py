# ---------------------------------------------------------------------------
# Importações
# ---------------------------------------------------------------------------
from fastapi import FastAPI
from pydantic import BaseModel
from celery_app import calcular_soma, calcular_fatorial, consultar_tarefa

# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API",
    description="API para tarefas EBAC",
    version="1.0.0",
    contact={"name": "Luis Fernandes", "email": "luis.vidio9@gmail.com"},
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SomaRequest(BaseModel):
    num_a: int
    num_b: int

class FatorialRequest(BaseModel):
    num: int

# ---------------------------------------------------------------------------
# Rotas 
# ---------------------------------------------------------------------------
@app.post("/soma")
def criar_tarefa_soma(dados: SomaRequest):
    task = calcular_soma.delay(dados.num_a, dados.num_b)
    return {
        "mensagem": "Calculo de soma enviada para processamento",
        "task_id": task.id
    }

@app.post("/fatorial")
def criar_tarefa_fatorial(dados: FatorialRequest):
    task = calcular_fatorial.delay(dados.num)
    return {
        "mensagem": "Calculo de fatorial enviado para processamento",
        "task_id": task.id
    }

@app.get("/tarefas/{task_id}")
def consultar_tarefa_celery(task_id: str):
    return consultar_tarefa(task_id)