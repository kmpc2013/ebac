# API de Livros — Docker Architecture

Projeto do curso EBAC Backend: API FastAPI para gerenciamento de catálogo de livros, containerizada com Docker.

## Componentes

| Componente | Forma | Cor | Descrição |
|---|---|---|---|
| **main.py** | Nota (post-it) | Verde | Código-fonte da aplicação FastAPI com rotas CRUD, SQLAlchemy, Redis cache e Celery tasks |
| **Dockerfile** | Documento | Azul | Instruções de build: base image Python 3.14-slim, instalação de dependências com `uv`, exposição da porta 8000 |
| **docker-compose.yml** | Nota (post-it) | Amarelo | Define os 3 serviços (api, redis, celery), portas, volumes e variáveis de ambiente |
| **docker-compose up -d** | Triângulo | Vermelho | Comando que orquestra a criação e execução dos containers |
| **Imagem Docker** | Hexágono | Roxo | Artefato imutável contendo Python, uv, main.py e dependências |
| **Containers** | Retângulo arredondado | Laranja | Instâncias em execução: api-livros, livros-redis, livros-celery |
| **Porta 8000** | Elipse | Azul claro | Ponto de acesso externo mapeado do host para o container |
| **Cliente Externo** | Ícone pessoa | Verde | Navegador, cURL ou frontend que consome a API |

## Relações entre Componentes

| Origem | Destino | Tipo | Descrição |
|---|---|---|---|
| main.py | Dockerfile | `COPY` | O Dockerfile copia o código-fonte para dentro da imagem |
| docker-compose.yml | docker-compose up | Sólido | O compose dispara o comando de orquestração |
| docker-compose up | Dockerfile | Sólido | O build invoca o Dockerfile para criar a imagem |
| docker-compose up | Containers | Sólido | Cria e gerencia os 3 containers |
| Dockerfile | Imagem Docker | Sólido | O Dockerfile gera a imagem final |
| Imagem Docker | Container API | Sólido | A imagem é executada como container |
| Imagem Docker | Container Celery | Sólido | A imagem é executada como container |
| Container API | Porta 8000 | Sólido | Mapeamento `8000:8000` do container para o host |
| Container Celery | Container Redis | Tracejado | `depends_on` — Celery aguarda o Redis |
| Container API | Container Redis | Tracejado | `depends_on` — API aguarda o Redis |
| main.py | Container API | Traceado | O código fonte é o conteúdo executado no container |
| Cliente Externo | Porta 8000 | Sólido | Requisições HTTP (GET, POST, PUT, DELETE) |

## Mapeamento de Portas

| Serviço | Porta (Host) | Porta (Container) | Exposição |
|---|---|---|---|
| API (FastAPI) | 8000 | 8000 | Acesso externo via HTTP |
| Redis | 6379 | 6379 | Cache e filas de mensagens |
| Celery | — | — | Worker interno, sem porta exposta |

## Fluxo de Execução

```
1. docker-compose.yml define os 3 serviços (redis, celery, api)
         │
         ▼
2. docker-compose executa "build: ." para cada serviço
         │
         ▼
3. Dockerfile é processado → cria a Imagem Docker (myapp:latest)
         │
         ▼
4. Containers são iniciados (redis, celery, api)
         │
         ▼
5. Porta 8000 é mapeada do container para o host
         │
         ▼
6. Cliente envia requisição HTTP para http://localhost:8000
         │
         ├──► GET /livros        → Consulta SQLite + Cache Redis
         ├──► POST /adiciona     → Insere no SQLite + Redis
         ├──► PUT /atualiza/{id} → Atualiza registro
         └──► DELETE /deletar/{id} → Remove registro
```

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) (ou Docker Desktop)

## Como Executar

```bash
# Construir as imagens
docker compose build

# Iniciar os containers
docker compose up -d

# Verificar status
docker compose ps

# Acessar a API
curl http://localhost:8000

# Parar os containers
docker compose down
```

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Health check (Hello World) |
| GET | `/livros` | Lista livros (com paginação) |
| POST | `/adiciona` | Adiciona um livro |
| PUT | `/atualiza/{id}` | Atualiza um livro |
| DELETE | `/deletar/{id}` | Deleta um livro |
| POST | `/celery/soma` | Envia tarefa de soma para Celery |
| POST | `/celery/fatorial` | Envia tarefa de fatorial para Celery |
| GET | `/debug/redis` | Visualiza chaves no Redis |

## Tecnologias

- **FastAPI** — Framework web assíncrono
- **SQLAlchemy** — ORM para SQLite
- **Redis** — Cache e broker de mensagens
- **Celery** — Processamento assíncrono de tarefas
- **Docker** — Containerização
- **Docker Compose** — Orquestração de múltiplos containers
- **uv** — Gerenciador de pacotes Python
