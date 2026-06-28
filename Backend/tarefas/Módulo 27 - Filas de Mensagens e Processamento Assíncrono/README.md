# FastAPI com Celery e Redis

Projeto da atividade do modulo 27 usando FastAPI, Celery e Redis para executar tarefas demoradas em background.

## Requisitos

- Python 3.11+
- Docker
- Dependencias do `requirements.txt`

## Instalacao

```bash
pip install -r requirements.txt
```

## Subir o Redis

O Redis roda em container e fica exposto na porta `6379`.

```bash
docker compose up -d
```

O Celery usa o Redis como broker e backend:

```text
redis://localhost:6379/0
```

## Rodar o worker Celery

Como estou executando o worker localmente no Windows, uso o `--pool=solo`:

```bash
celery -A celery_app worker -l info --pool=solo
```

## Rodar a API

```bash
uvicorn app:app --reload
```

A documentacao da API fica em:

```text
http://localhost:8000/docs
```

## Testes

Enviar tarefa de soma:

```bash
curl -X POST http://localhost:8000/soma -H "Content-Type: application/json" -d "{\"num_a\": 10, \"num_b\": 5}"
```

Enviar tarefa de fatorial:

```bash
curl -X POST http://localhost:8000/fatorial -H "Content-Type: application/json" -d "{\"num\": 5}"
```

Consultar resultado da tarefa:

```bash
curl http://localhost:8000/tarefas/SEU_TASK_ID
```

## Evidencias

Worker conectado ao Redis:

```text
[2026-06-28 10:13:41,368: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-06-28 10:13:42,443: INFO/MainProcess] celery@SCPNOTE138 ready.
```

Exemplo de retorno ao criar uma tarefa:

```json
{
  "mensagem": "Calculo de soma enviada para processamento",
  "task_id": "id-da-tarefa"
}
```

Exemplo de consulta apos o processamento:

```json
{
  "task_id": "id-da-tarefa",
  "status": "SUCCESS",
  "resultado": 15
}
```

Os endpoints `POST` apenas enviam a tarefa para o Celery com `.delay()` e retornam o `task_id`, sem esperar o calculo terminar.
