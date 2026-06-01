FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-install-project --no-dev

COPY main.py ./

RUN uv sync --frozen --no-dev

RUN touch livros.db

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
