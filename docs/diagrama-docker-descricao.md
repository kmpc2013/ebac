# Diagrama de Arquitetura Docker — Projeto EBAC Backend

> Arquivo de referência: `diagrama-docker.drawio`

---

## Componentes do Diagrama

### 1. main.py
- **Forma:** Nota (post-it)
- **Cor:** Verde (`#d5e8d4`)
- **Conteúdo:** Aplicação FastAPI + Uvicorn com rotas CRUD, SQLAlchemy, Redis cache e Celery tasks
- **Localização no diagrama:** Parte inferior central do bloco HOST

### 2. Dockerfile
- **Forma:** Documento
- **Cor:** Azul (`#dae8fc`)
- **Conteúdo:** Instruções de build da imagem — FROM python:3.14-slim, WORKDIR /app, COPY dos arquivos, RUN poetry install, EXPOSE 8000, CMD uvicorn
- **Localização no diagrama:** Centro do bloco HOST

### 3. docker-compose.yml
- **Forma:** Nota (post-it)
- **Cor:** Amarelo (`#fff2cc`)
- **Conteúdo:** Definição dos 3 serviços — redis, celery e api
- **Localização no diagrama:** Lado esquerdo do bloco HOST

### 4. docker-compose up -d
- **Forma:** Triângulo
- **Cor:** Vermelho (`#f8cecc`)
- **Significado:** Comando/orquestração que dispara a criação dos containers
- **Localização no diagrama:** Entre o docker-compose.yml e os containers

### 5. Imagem Docker
- **Forma:** Hexágono
- **Cor:** Roxo (`#e1d5e7`)
- **Conteúdo:** Imagem final com Python 3.14-slim, poetry, main.py, livros.db e dependências
- **Localização no diagrama:** Centro-direita do bloco HOST

### 6. Containers (3 unidades)
- **Forma:** Retângulo arredondado
- **Cor:** Laranja (`#ffe6cc`)

| Container | Nome | Porta | Observação |
|---|---|---|---|
| Redis | livros-redis | 6379:6379 | Serviço de cache |
| Celery | livros-celery | — (worker interno) | Processa tarefas assíncronas |
| API | api-livros | 8000:8000 | Aplicação FastAPI |

### 7. Porta 8000 (Host)
- **Forma:** Elipse
- **Cor:** Azul claro (`#dae8fc`)
- **Significado:** Ponto de acesso externo ao container da API

### 8. Cliente Externo
- **Forma:** Ícone de pessoa (actor)
- **Cor:** Verde (`#d5e8d4`)
- **Conteúdo:** Navegador Web, cURL / Postman, Frontend (React)
- **Localização:** Fora do bloco HOST (parte inferior)

---

## Relações e Conexões

| ID | Origem | Destino | Estilo | Rótulo | Significado |
|---|---|---|---|---|---|
| arrow1 | main.py | Dockerfile | Tracejado verde | `COPY` | O Dockerfile copia o main.py para dentro da imagem |
| — | docker-compose.yml | docker-compose up -d | Sólido laranja | — | O compose dispara o comando de subida |
| — | docker-compose up -d | Dockerfile | Sólido azul | — | O build invoca o Dockerfile para criar a imagem |
| — | docker-compose up -d | Container Redis | Sólido laranja | — | Cria o container Redis |
| — | docker-compose up -d | Container Celery | Sólido laranja | — | Cria o container Celery |
| — | docker-compose up -d | Container API | Sólido laranja | — | Cria o container da API |
| — | Dockerfile | Imagem Docker | Sólido roxo | — | O Dockerfile gera a imagem Docker |
| — | Imagem Docker | Container API | Sólido laranja | — | A imagem é executada como container |
| — | Imagem Docker | Container Celery | Sólido laranja | — | A imagem é executada como container |
| arrow7 | Container API | Porta 8000 | Sólido azul | `8000:8000` | Mapeamento da porta do container para o host |
| arrow8 | Container Celery | Container Redis | Tracejado laranja | `depends_on` | Celery depende do Redis para funcionar |
| arrow8b | Container API | Container Redis | Tracejado laranja | `depends_on` | API depende do Redis para cache |
| arrow11 | main.py | Container API | Tracejado roxo | `conteúdo` | O código fonte é o conteúdo executado no container |
| arrow10 | Cliente Externo | Porta 8000 | Sólido verde | `HTTP Request` | Cliente envia requisições para a API |

---

## Fluxo de Execução

```
1. docker-compose.yml define os 3 serviços (redis, celery, api)
         │
         ▼
2. docker-compose executa "build: ." em cada serviço
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
6. Cliente acessa http://localhost:8000
         │
         ├──► GET /livros       → Consulta SQLite + Cache Redis
         ├──► POST /adiciona    → Insere no SQLite + Redis
         ├──► PUT /atualiza/{id}→ Atualiza registro
         └──► DELETE /deletar/{id} → Remove registro
```

---

## Mapeamento de Portas

| Serviço | Porta (Host) | Porta (Container) | Observação |
|---|---|---|---|
| API (FastAPI) | 8000 | 8000 | Acesso externo via HTTP |
| Redis | 6379 | 6379 | Cache e filas |
| Celery | — | — | Worker interno, sem porta exposta |

---

## Legenda de Formas

| Forma | Cor | Representa |
|---|---|---|
| Nota (post-it) | Verde | Arquivo fonte (`main.py`) |
| Documento | Azul | Configuração Docker (`Dockerfile`) |
| Nota (post-it) | Amarelo | Orquestração (`docker-compose.yml`) |
| Triângulo | Vermelho | Ação / Comando Docker |
| Hexágono | Roxo | Imagem Docker |
| Retângulo arredondado | Laranja | Container em execução |
| Elipse | Azul claro | Porta mapeada no host |
| Ícone pessoa | Verde | Cliente externo |
