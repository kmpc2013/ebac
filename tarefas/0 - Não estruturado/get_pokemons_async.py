# Atividade: simulador de captura de pokemons usando async/await
import asyncio
import random
import time


def pokemon_aleatorio(regiao):
    # pega um pokemon aleatorio da regiao
    pokemons = {
        "kanto": ["bulbasaur", "charmander", "squirtle", "pikachu", "raichu",],
        "johto": ["cyndaquil", "totodile", "chikorita",],
        "hoenn": ["treecko", "torchic", "mudkip", "turtwig", "chimchar"],
    }
    return random.choice(pokemons[regiao])


# funcoes async pra cada regiao - rodam ao mesmo tempo com o gather
async def busca_pokemon_kanto():
    print("Buscando Pokémon em Kanto...")
    await asyncio.sleep(random.uniform(1, 5))  # simula demora da busca
    return pokemon_aleatorio("kanto")


async def busca_pokemon_johto():
    print("Buscando Pokémon em Johto...")
    await asyncio.sleep(random.uniform(1, 5))
    return pokemon_aleatorio("johto")


async def busca_pokemon_hoenn():
    print("Buscando Pokémon em Hoenn...")
    await asyncio.sleep(random.uniform(1, 5))
    return pokemon_aleatorio("hoenn")


async def main():
    inicio = time.perf_counter()

    # gather roda as 3 buscas juntas e devolve os resultados
    kanto, johto, hoenn = await asyncio.gather(
        busca_pokemon_kanto(),
        busca_pokemon_johto(),
        busca_pokemon_hoenn(),
    )

    print(f"Pokémon encontrado em Kanto: {kanto}")
    print(f"Pokémon encontrado em Johto: {johto}")
    print(f"Pokémon encontrado em Hoenn: {hoenn}")
    
    tempo_execucao = time.perf_counter() - inicio  # tempo da busca (vai ser perto do maior sleep)
    print(f"Tempo total de execução: {tempo_execucao:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(main())
