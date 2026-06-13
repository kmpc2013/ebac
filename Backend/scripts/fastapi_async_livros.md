# API de Livros (async)

Atividade do curso EBAC — CRUD de livros com FastAPI usando `async/await`.
Os dados ficam em memória, sem banco.

Arquivo da API: `fastapi_async_livros.py`

## Dependências

- Python 3.14+
- fastapi
- uvicorn

## Como rodar
Como é um projeto sem muitas dependências, podemos rodar direto com pip.

```bash
pip install fastapi uvicorn
cd scripts
uvicorn fastapi_async_livros:app --reload
```

A API sobe em `http://127.0.0.1:8000`. Docs interativas: http://127.0.0.1:8000/docs

## Endpoints

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/livros` | Lista todos os livros |
| POST | `/livros` | Cria um livro |
| PUT | `/livros/{id_livro}` | Atualiza um livro |
| DELETE | `/livros/{id_livro}` | Remove um livro |

Body do POST/PUT (JSON):

```json
{
  "nome_livro": "1984",
  "autor_livro": "George Orwell",
  "ano_livro": 1949
}
```

## Testando com curl

```bash
# listar livros
curl http://127.0.0.1:8000/livros

# criar livro
curl -X POST http://127.0.0.1:8000/livros \
  -H "Content-Type: application/json" \
  -d "{\"nome_livro\":\"1984\",\"autor_livro\":\"George Orwell\",\"ano_livro\":1949}"

# atualizar livro (id 1)
curl -X PUT http://127.0.0.1:8000/livros/1 \
  -H "Content-Type: application/json" \
  -d "{\"nome_livro\":\"1984\",\"autor_livro\":\"George Orwell\",\"ano_livro\":1950}"

# deletar livro (id 1)
curl -X DELETE http://127.0.0.1:8000/livros/1

# erro 404 — livro que não existe
curl -X DELETE http://127.0.0.1:8000/livros/999
```
