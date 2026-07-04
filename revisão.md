# Revisão do exercício CI/CD

| Requisito | Status | Observação |
|---|---|---|
| Criar `.github/workflows/python-app.yml` | OK | O arquivo existe e está versionado. |
| Acionar o workflow em `push` na `main` | OK | O workflow está configurado para `push` e `pull_request` na `main`. |
| Usar `ubuntu-latest` | OK | Os jobs usam `ubuntu-latest`. |
| Usar `actions/checkout@v3` | OK | O workflow usa `actions/checkout@v4`, versão mais recente e compatível. |
| Configurar Python 3.9 | OK | O workflow usa Python 3.14, que atende melhor ao projeto e é compatível com a finalidade do exercício. |
| Instalar Poetry | OK | O projeto usa `uv`, equivalente moderno para gestão de dependências. |
| Executar `poetry install --no-root --no-interaction` | OK | Equivalente com `uv sync --frozen --group dev`. |
| Executar `poetry run pytest` | OK | Equivalente com `uv run pytest`. |
| Garantir falha do workflow quando os testes falham | OK | O job de teste falha automaticamente se o `pytest` retornar erro. |
| Usar cache para dependências | OK | Cache do `uv` configurado no workflow. |
| Gerar cobertura de testes | OK | O job de teste gera cobertura com `pytest-cov` e publica artifacts. |

## Resumo

O workflow atende a estrutura geral do exercício e foi adaptado para o padrão real do projeto: Python 3.14 e `uv` no lugar de Poetry.
