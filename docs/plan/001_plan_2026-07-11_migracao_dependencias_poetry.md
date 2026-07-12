# Objective

Migrar o projeto raiz do backend para Poetry, mantendo o comportamento atual de dependências, testes, build Docker e execução no CI.

# Proposed Solution

Substituir o fluxo de gerenciamento de dependências do projeto raiz por Poetry, gerar `poetry.lock` e atualizar os pontos de integração.

O ajuste deve ficar restrito ao projeto principal em `Backend/`, preservando subprojetos e materiais de tarefa que não façam parte do fluxo ativo.

# Impact

- Rating: 7/10
- Justificativa: mudança simples na lógica do app, mas com impacto em empacotamento, CI, Docker e documentação.
- Components affected:
  - dependency management
  - GitHub Actions
  - Docker build/runtime
  - root documentation
- Files likely to change:
  - `pyproject.toml`
  - `poetry.lock`
  - `Dockerfile`
  - `docker-compose.yml`
  - `.github/workflows/python-app.yml`
  - `docs/*.md` and `docs/*.drawio` with migration references
- External dependencies:
  - Poetry

# Risks

- Dependency resolution can differ between managers.
  - Mitigation: regenerate the lockfile and run tests/lint after migration.
- Docker image may fail if Poetry is not installed or the virtualenv path differs.
  - Mitigation: pin Poetry in the image and keep the in-project virtualenv path explicit.
- CI can break because the commands and cache keys change.
  - Mitigation: update workflow commands and validate the full pipeline.

# Acceptance Criteria

- The root project installs dependencies using Poetry only.
- `poetry.lock` exists and is consistent with `pyproject.toml`.
- The Docker image builds successfully with Poetry.
- The GitHub Actions workflow runs lint and tests with Poetry.
- Root documentation and runtime config no longer depend on the previous manager.

# Implementation Steps

1. Convert the root project metadata to Poetry-compatible configuration.
2. Generate `poetry.lock` from the current dependency set.
3. Update `Dockerfile` and `docker-compose.yml` to use Poetry/runtime commands.
4. Update the GitHub Actions workflow to install and use Poetry.
5. Replace root docs and diagrams that mention the previous manager.
6. Run lint, tests, and container build to verify the migration.
