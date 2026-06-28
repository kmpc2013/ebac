# ---------------------------------------------------------------------------
# Importações
# ---------------------------------------------------------------------------
from celery import Celery
from celery.result import AsyncResult
import os
import time

# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

celery_app = Celery(
    "tarefas_livros",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
    result_persistent=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

# ---------------------------------------------------------------------------
# Funcoes 
# ---------------------------------------------------------------------------
@celery_app.task
def calcular_soma(a: int, b: int):
    time.sleep(1)
    return a + b

@celery_app.task
def calcular_fatorial(numero: int):
    if numero < 0:
        raise ValueError("Não existe fatorial de número negativo")
    time.sleep(1)
    resultado = 1
    for i in range(2, numero + 1):
        resultado *= i
    return resultado

def consultar_tarefa(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    resposta = {
        "task_id": task_id,
        "status": task.status,
    }
    if task.ready():
        resposta["resultado"] = task.result
    return resposta