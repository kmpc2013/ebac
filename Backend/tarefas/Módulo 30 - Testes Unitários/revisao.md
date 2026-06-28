# Plano de Atividade — Módulo 30: Testes Unitários

| # | Task | Status | Observação |
|---|---|---|---|
| 1 | Criar `pokemon.py` com as funções `calcula_pontos_ataque` e `pokemon_evolui` | NAO | Implementar funções conforme enunciado |
| 2 | Criar `test_pokemon.py` com estrutura básica de testes | NAO | Arquivo de testes ainda não existe |
| 3 | Criar fixture p/ Pokémon (ex: Pikachu) com `@pytest.fixture` | NAO | Retornar dict com "nome", "forca_base", "nivel" |
| 4 | Criar fixture p/ outro Pokémon (ex: Charmander) com `@pytest.fixture` | NAO | Segunda fixture para diversidade de dados |
| 5 | Criar fixture p/ Pokémon de nível baixo (ex: Caterpie) | NAO | Opcional — cobre borda de evolução |
| 6 | Testar `calcula_pontos_ataque` com as fixtures | NAO | Verificar cálculo (ex: forca_base * nivel) |
| 7 | Testar `pokemon_evolui` com Pokémon que pode evoluir | NAO | Ex: nível >= 16 retorna True |
| 8 | Testar `pokemon_evolui` com Pokémon que NÃO pode evoluir | NAO | Ex: nível < 16 retorna False |
| 9 | Testar `pokemon_evolui` no limite (nível == 16) | NAO | Caso de borda |
| 10 | Código comentado e organizado | NAO | Adicionar docstrings/comentários |
| 11 | Executar `pytest test_pokemon.py` e verificar passagem | NAO | Validar que todos os testes passam |
