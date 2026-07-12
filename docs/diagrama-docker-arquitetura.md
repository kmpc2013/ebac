# Diagrama de Arquitetura Docker — Projeto EBAC Backend

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           MÁQUINA HOST (Seu Computador)                                  │
│                                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                              │
│   │   main.py    │    │ Dockerfile   │    │docker-compose│                              │
│   │  (FastAPI)   │    │  (Receita)   │    │    .yml      │                              │
│   │              │    │              │    │ (Orquestra)   │                              │
│   │ • Rotas CRUD │    │ • Base image │    │              │                              │
│   │ • Redis      │    │ • Deps       │    │ • Serviços   │                              │
│   │ • Celery     │    │ • Copia main │    │ • Portas     │                              │
│   │ • SQLite     │    │ • Expõe 8000 │    │ • Volumes    │                              │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                              │
│          │                   │                   │                                       │
│          │    ┌──────────────┴───────────────┐   │                                       │
│          │    │                              │   │                                       │
│          │    │     docker build -t myapp .   │   │                                       │
│          │    │                              │   │                                       │
│          │    └──────────────┬───────────────┘   │                                       │
│          │                   │                   │                                       │
│          │                   ▼                   │                                       │
│          │    ┌──────────────────────────────┐   │                                       │
│          │    │       IMAGEM DOCKER          │   │                                       │
│          │    │       myapp:latest           │   │                                       │
│          │    │                              │   │                                       │
│          │    │  ┌────────────────────────┐  │   │                                       │
│          │    │  │  Python 3.14-slim      │  │   │                                       │
│          │    │  │  + poetry (gerenciador)│  │   │                                       │
│          │    │  │  + main.py             │  │   │                                       │
│          │    │  │  + livros.db           │  │   │                                       │
│          │    │  │  + dependências        │  │   │                                       │
│          │    │  └────────────────────────┘  │   │                                       │
│          │    └──────────────┬───────────────┘   │                                       │
│          │                   │                   │                                       │
│          │                   │ docker-compose    │                                       │
│          │                   │ up -d             │                                       │
│          │                   ▼                   │                                       │
│          │    ┌──────────────────────────────────────────────────────────────────┐       │
│          │    │                    DOCKER COMPOSE                                │       │
│          │    │                                                                  │       │
│          │    │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │       │
│          │    │   │    redis        │  │     celery      │  │      api        │ │       │
│          │    │   │   container     │  │    container    │  │    container    │ │       │
│          │    │   │                 │  │                 │  │                 │ │       │
│          │    │   │ redis:latest    │  │  build: .       │  │   build: .      │ │       │
│          │    │   │                 │  │                 │  │                 │ │       │
│          │    │   │  Porta:         │  │  Comando:       │  │  Porta:         │ │       │
│          │    │   │  6379:6379      │  │  celery worker  │  │  8000:8000      │ │       │
│          │    │   │                 │  │                 │  │                 │ │       │
│          │    │   │  Volumes:       │  │  Volumes:       │  │  Env:           │ │       │
│          │    │   │  (nenhum)       │  │  .:/app         │  │  DATABASE_URL   │ │       │
│          │    │   │                 │  │  celery_venv    │  │  REDIS_URL      │ │       │
│          │    │   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │       │
│          │    │            │                    │                    │          │       │
│          │    │            │   depends_on       │                    │          │       │
│          │    │            └────────────────────┘                    │          │       │
│          │    │                                                     │          │       │
│          │    └─────────────────────────────────────────────────────────────────┘       │
│          │                                                                              │
│          │                                                                              │
│          │    ╔═══════════════════════════════════════════════════════════════════╗      │
│          │    ║                    FLUXO DE REQUISIÇÕES                           ║      │
│          │    ╚═══════════════════════════════════════════════════════════════════╝      │
│          │                                                                              │
└──────────┼──────────────────────────────────────────────────────────────────────────────┘
           │
           │  http://localhost:8000
           │
           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                          │
│                        ┌───────────────────────────┐                                     │
│                        │      CLIENTE EXTERNO      │                                     │
│                        │                           │                                     │
│                        │  • Navegador Web          │                                     │
│                        │  • cURL / Postman         │                                     │
│                        │  • Frontend (React, etc)  │                                     │
│                        └─────────────┬─────────────┘                                     │
│                                      │                                                   │
│                                      │  GET /livros                                      │
│                                      │  POST /adiciona                                   │
│                                      │  PUT /atualiza/{id}                               │
│                                      │  DELETE /deletar/{id}                             │
│                                      │                                                   │
│                                      ▼                                                   │
│                        ┌───────────────────────────┐                                     │
│                        │   Porta 8000 (Host)       │                                     │
│                        │          │                │                                     │
│                        │          ▼                │                                     │
│                        │   Porta 8000 (Container)  │                                     │
│                        │          │                │                                     │
│                        │          ▼                │                                     │
│                        │   uvicorn main:app        │                                     │
│                        │   --host 0.0.0.0          │                                     │
│                        └───────────────────────────┘                                     │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Legenda de Formas Geométricas

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              LEGENDA                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ╔══════════════════════╗     Arquivo Fonte / Configuração                     │
│   ║   Retângulo Sólido   ║     (main.py, Dockerfile, docker-compose.yml)       │
│   ╚══════════════════════╝                                                     │
│                                                                                 │
│   ┌──────────────────────┐     Processo / Comando                               │
│   │   Retângulo Tracejado│     (docker build, docker-compose up)               │
│   └──────────────────────┘                                                     │
│                                                                                 │
│   ╔══════════════════════╗     Componente Docker                                │
│   ║  Retângulo Borda     ║     (Container, Imagem Docker)                       │
│   ║  Dupla               ║                                                     │
│   ╚══════════════════════╝                                                     │
│                                                                                 │
│   ┌──────────────────────┐     Entidade Externa                                 │
│   │  Losango / Círculo   ║     (Cliente, Navegador)                             │
│   └──────────────────────┘                                                     │
│                                                                                 │
│   ───────────────────────►     Fluxo de Dados / Conexão                        │
│                                                                                 │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─►     Dependência / Relacionamento                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Tabela de Portas

```
┌────────────────┬────────────────┬────────────────────────────────┐
│   Serviço      │ Porta (Host)   │ Porta (Container)              │
├────────────────┼────────────────┼────────────────────────────────┤
│   API (FastAPI)│     8000       │     8000                       │
│   Redis        │     6379       │     6379                       │
│   Celery       │      -         │      - (worker interno)        │
└────────────────┴────────────────┴────────────────────────────────┘
```

## Fluxo de Execução

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. docker-compose.yml define os 3 serviços: redis, celery, api               │
│                          │                                                      │
│                          ▼                                                      │
│  2. docker-compose executa "build: ." para cada serviço                        │
│                          │                                                      │
│                          ▼                                                      │
│  3. Dockerfile é processado:                                                   │
│     ┌──────────────────────────────────────────────────────────────────┐       │
│     │  FROM python:3.14-slim-bookworm                                  │       │
│     │  RUN python -m pip install poetry                                │       │
│     │  WORKDIR /app                                                    │       │
│     │  COPY pyproject.toml poetry.lock ./                               │       │
│     │  RUN poetry install --only main --no-root                        │       │
│     │  COPY main.py ./                                                 │       │
│     │  EXPOSE 8000                                                     │       │
│     │  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]│     │
│     └──────────────────────────────────────────────────────────────────┘       │
│                          │                                                      │
│                          ▼                                                      │
│  4. Imagem Docker myapp:latest é criada                                        │
│                          │                                                      │
│                          ▼                                                      │
│  5. Containers são iniciados:                                                  │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                         │
│     │livros-redis │  │livros-celery│  │  api-livros  │                         │
│     │  :6379      │  │  (worker)   │  │   :8000      │                         │
│     └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                         │
│            │                │                │                                 │
│            │  ◄─────────────┘  conecta ao    │                                 │
│            │                  Redis           │                                 │
│            │                                 │                                 │
│            │  ◄──────────────────────────────┘                                 │
│            │  main.py usa redis para cache                                     │
│                          │                                                      │
│                          ▼                                                      │
│  6. Cliente acessa http://localhost:8000                                       │
│     │                                                                          │
│     ├─► GET /livros ──► Consulta SQLite + Cache Redis                          │
│     ├─► POST /adiciona ──► Insere no SQLite + Redis                            │
│     ├─► PUT /atualiza/{id} ──► Atualiza registro                               │
│     └─► DELETE /deletar/{id} ──► Remove registro                               │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```
