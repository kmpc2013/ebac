import pytest
from pokemon import calcula_pontos_ataque, pokemon_evolui

@pytest.fixture
def bulbasaur():
    return {"nome": "Bulbasaur", "forca_base": 49, "nivel": 10}

@pytest.fixture
def charmander():
    return {"nome": "Charmander", "forca_base": 52, "nivel": 15}

def test_calcula_pontos_ataque_bulbasaur(bulbasaur):
    assert calcula_pontos_ataque(bulbasaur) == 490

def test_pokemon_evoluiu_charmander(charmander):
    assert pokemon_evolui(charmander, 20) is False
    assert pokemon_evolui(charmander, 15) is True