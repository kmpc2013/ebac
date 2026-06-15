from celery_app import celery_app
import time

@celery_app.task(name="task.somar", bind=True)
def somar(self, a, b):
    time.sleep(5)
    return a+b

@celery_app.task(name="task.fatorial", bind=True)
def fatorial(self, n):
    time.sleep(5)
    if n < 0:
        raise ValueError("O número deve ser positivo")
    resultado = 1
    for i in range(2, n+1):
        resultado *= i
    return resultado

