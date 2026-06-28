def calcula_pontos_ataque(pokemon):
    return pokemon["forca_base"] * pokemon["nivel"]

def pokemon_evolui(pokemon, nivel_evolucao):
    return pokemon["nivel"] >= nivel_evolucao

