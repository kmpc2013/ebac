import pytest
from pokemon import calcula_pontos_ataque, pokemon_evolui

def test_calcula_pontos_ataque_forca10_nivel1():
    pokemon = {"forca_base": 10, "nivel": 1}
    resultado = calcula_pontos_ataque(pokemon)
    assert resultado == 10

def test_calcula_pontos_ataque_forca5_nivel0():
    pokemon = {"forca_base": 5, "nivel": 0}
    resultado = calcula_pontos_ataque(pokemon)
    assert resultado == 0

def test_calcula_pontos_ataque_forca20_nivel5():
    pokemon = {"forca_base": 20, "nivel": 5}
    resultado = calcula_pontos_ataque(pokemon)
    assert resultado == 100

def test_calcula_pontos_ataque_forca_negativa():
    pokemon = {"forca_base": -3, "nivel": 4}
    resultado = calcula_pontos_ataque(pokemon)
    assert resultado == -12

def test_pokemon_nao_evolui_nivel_menor():
    pokemon = {"nivel": 15}
    resultado = pokemon_evolui(pokemon, 20)
    assert resultado is False

def test_pokemon_evolui_nivel_igual():
    pokemon = {"nivel": 20}
    resultado = pokemon_evolui(pokemon, 20)
    assert resultado is True

def test_pokemon_evolui_nivel_maior():
    pokemon = {"nivel": 25}
    resultado = pokemon_evolui(pokemon, 20)
    assert resultado is True

def test_pokemon_evolui_nivel_zero_evolucao_zero():
    pokemon = {"nivel": 0}
    resultado = pokemon_evolui(pokemon, 0)
    assert resultado is True