# ebac

API FastAPI de livros (Backend EBAC).

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado
- Python 3.14+ (`uv python install 3.14` se necessário)

## Desenvolvimento local

```bash
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Comandos úteis

| Ação | Comando |
|------|---------|
| Instalar dependências | `uv sync` |
| Adicionar pacote | `uv add <pacote>` |
| Atualizar lockfile | `uv lock` |
| Rodar comando no venv | `uv run <comando>` |

## Docker

```bash
docker compose build
docker compose up
```

A API fica em http://localhost:8000.
