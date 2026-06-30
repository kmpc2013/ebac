# API de Livros com FastAPI e Redis

Projeto simples de API para cadastro de livros usando FastAPI e Redis como cache.

## Requisitos

- Python 3.11+
- Redis instalado localmente ou Docker
- Dependencias do `requirements.txt`

## Instalacao

```bash
pip install -r requirements.txt
```

## Executando o Redis

### Opcao 1: Docker

```bash
docker compose up -d
```

### Opcao 2: Redis local

Se ja tiver o Redis instalado localmente, basta iniciar o servico na porta padrao:

```bash
redis-server
```

A aplicacao usa por padrao:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_TTL=60
```

## Executando a API

```bash
uvicorn app:app --reload
```

A API ficara disponivel em:

```text
http://localhost:8000
```

A documentacao automatica fica em:

```text
http://localhost:8000/docs
```

## Endpoints principais

- `GET /livros` - lista os livros, usando cache do Redis quando disponivel
- `POST /livros` - cadastra um livro
- `PUT /livros/{id_livro}` - atualiza um livro
- `DELETE /livros/{id_livro}` - remove um livro
- `GET /livros/redis` - mostra o conteudo salvo no Redis

## Exemplo de livro

```json
{
  "nome_livro": "Dom Casmurro",
  "autor_livro": "Machado de Assis",
  "ano_livro": 1899
}
```

## Conferindo o Redis pelo Docker

```bash
docker exec -it livros-redis redis-cli
```

Dentro do Redis:

```redis
GET livros
TTL livros
```
