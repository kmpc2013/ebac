# Procedimento do programa:
# Adicionar Pokémon: O programa deve pedir o nome do Pokémon, o tipo (como "Fogo", "Água", "Elétrico", etc.), 
# e o nível (um número inteiro entre 1 e 100). Essas informações devem ser armazenadas no dicionário.

# Listar Pokémon: O programa deve exibir todos os Pokémon cadastrados no formato: nome do Pokémon - tipo - nível. 
# Os Pokémon devem ser listados em ordem alfabética.

# Remover Pokémon: O programa deve pedir o nome do Pokémon a ser removido. Caso o Pokémon exista, ele será removido do dicionário. 
# Se o Pokémon não existir, o programa exibirá uma mensagem de erro.

# Atualizar nível do Pokémon: O programa deve pedir o nome do Pokémon e o novo nível (um número inteiro entre 1 e 100). 
# Se o Pokémon existir, o nível será atualizado. Caso contrário, será exibida uma mensagem de erro.

# Registrar captura de Pokémon: O programa deve pedir o nome do Pokémon e a quantidade de vezes capturadas. 
# O valor de capturas será atualizado, aumentando a quantidade de vezes que o Pokémon foi capturado. 
# Caso o Pokémon não exista, será exibida uma mensagem de erro.

# Exibir histórico de capturas: O histórico de capturas deve ser armazenado em uma lista, 
# onde cada entrada consiste no nome do Pokémon e a quantidade de vezes que foi capturado. 
# Quando o usuário escolher exibir o histórico de capturas, o programa deve mostrar todas as entradas feitas.

# Sair: O programa deve encerrar sua execução quando o usuário escolher a opção de sair.
# ---

def obter_dados_pokemon(pokemon_nome, pokemon_tipo, pokemon_nivel):
    """
    Função para formatar os dados de um Pokémon em uma string.
    O aluno deve retornar uma string formatada com os parâmetros nome, tipo e nível.
    """
    return f"{pokemon_nome} {pokemon_tipo} {pokemon_nivel}"

def obter_nivel_pokemon(nivel):
    """
    Função para obter e validar o nível do Pokémon.
    O aluno deve converter a entrada para inteiro e verificar se está entre 1 e 100.
    Em caso de erro, deve retornar uma mensagem específica.
    """
    try:
        nivel_int = int(nivel)
        if 1 <= nivel_int <= 100:
            return nivel_int
        else:
            return "O nível deve estar entre 1 e 100. Tente novamente."
    except ValueError:
        return "O nível deve ser um número inteiro. Tente novamente."

def validar_pokemon_existe(pokedex, pokemon_nome):
    """
    Função para verificar se um Pokémon existe na Pokédex.
    O aluno deve verificar se o nome do Pokémon está nas chaves do dicionário pokedex.
    Se não existir, retornar uma mensagem de erro.
    """
    if pokemon_nome in pokedex:
        return True
    return f"Erro: O Pokémon '{pokemon_nome}' não foi encontrado."

def adicionar_pokemon(pokedex, pokemon_nome, pokemon_tipo, pokemon_nivel):
    """
    Função para adicionar um novo Pokémon à Pokédex.
    O aluno deve verificar se o Pokémon já existe antes de adicioná-lo.
    Se não existir, deve adicionar um novo item ao dicionário pokedex com nome, tipo, nível e capturado (inicializado como 0).
    """
    if validar_pokemon_existe(pokedex, pokemon_nome) is True:
        return f"Erro: O Pokémon '{pokemon_nome}' já existe."
    pokedex[pokemon_nome] = {"tipo": pokemon_tipo, "nivel": pokemon_nivel, "capturado": 0}
    return f"Pokémon '{pokemon_nome}' adicionado com sucesso!"

def listar_pokemon(pokedex):
    """
    Função para listar todos os Pokémon cadastrados na Pokédex.
    O aluno deve verificar se a Pokédex está vazia. Se não, deve iterar sobre os itens da Pokédex,
    formatar as informações de cada Pokémon e retornar uma string com todos os Pokémon listados.
    """
    if not pokedex:
        return "Não há Pokémon cadastrados."
    resultado = []
    for pokemon_nome, pokemon_info in sorted(pokedex.items(), key=lambda x: x[0]):
        resultado.append(f"{pokemon_nome} - {pokemon_info['tipo']} - {pokemon_info['nivel']}")
    return "\n".join(resultado)

def remover_pokemon(pokedex, pokemon_nome):
    """
    Função para remover um Pokémon da Pokédex.
    O aluno deve primeiro validar se o Pokémon existe usando a função validar_pokemon_existe.
    Se existir, deve remover o item correspondente do dicionário pokedex.
    """
    validacao = validar_pokemon_existe(pokedex, pokemon_nome)
    if validacao is not True:
        return validacao
    del pokedex[pokemon_nome]
    return f"Pokémon '{pokemon_nome}' removido com sucesso!"

def atualizar_nivel_pokemon(pokedex, pokemon_nome, nivel):
    """
    Função para atualizar o nível de um Pokémon existente na Pokédex.
    O aluno deve primeiro validar se o Pokémon existe.
    Se existir, deve atualizar o valor da chave 'nivel' para o novo nível fornecido.
    """
    validacao = validar_pokemon_existe(pokedex, pokemon_nome)
    if validacao is not True:
        return validacao
    pokedex[pokemon_nome]["nivel"] = nivel
    return f"Nível do Pokémon '{pokemon_nome}' atualizado para {nivel}"

def registrar_captura(pokedex, historico_capturas, pokemon_nome, quantidade_capturas):
    """
    Função para registrar a captura de um ou mais Pokémon.
    O aluno deve validar se o Pokémon existe e se o número de capturas é maior que zero.
    Se as condições forem atendidas, deve adicionar o número de capturas à contagem existente do Pokémon
    e adicionar um registro ao histórico de capturas.
    """
    validacao = validar_pokemon_existe(pokedex, pokemon_nome)
    if validacao is not True:
        return validacao
    if quantidade_capturas <= 0:
        return f'Erro: Quantidade de capturas deve ser maior que 0.'
    pokedex[pokemon_nome]["capturado"] += quantidade_capturas
    historico_capturas.append((pokemon_nome, quantidade_capturas))
    return f"{quantidade_capturas} captura(s) registrada(s) para o Pokémon '{pokemon_nome}'."

def exibir_historico_capturas(historico_capturas):
    """
    Função para exibir o histórico de capturas de Pokémon.
    O aluno deve verificar se o histórico está vazio. Se não, deve formatar cada registro do histórico
    e retornar uma string com todas as capturas registradas.
    """
    if not historico_capturas:
        return "Não há histórico de capturas."
    return "\n".join([f"{idx}. {pokemon_nome} - {quantidade} captura(s)" for idx, (pokemon_nome, quantidade) in enumerate(historico_capturas, start=1)])

def exibir_menu():
    """
    Função para exibir as opções do menu para o usuário.
    O aluno deve retornar uma string com as opções formatadas.
    """
    return (
        "\n1. Adicionar Pokémon"
        "\n2. Listar Pokémon"
        "\n3. Remover Pokémon"
        "\n4. Atualizar nível do Pokémon"
        "\n5. Registrar captura de Pokémon"
        "\n6. Exibir histórico de capturas"
        "\n7. Sair"
    "\n")

def menu():
    """
    Função principal do programa (menu).
    O aluno deve inicializar a Pokédex (um dicionário) e o histórico de capturas (uma lista).
    Em seguida, deve entrar em um loop infinito para exibir o menu e processar a escolha do usuário.
    Cada opção do menu deve chamar a função correspondente.
    """
    pokedex = {}
    historico_capturas = []

    while True:
        print(exibir_menu())
        opcao = input("Escolha uma opção: ").strip()

        # 1. Adicionar Pokémon
        if opcao == '1':
            nome = input("Nome do Pokémon: ")
            tipo = input("Tipo do Pokémon: ")
            nivel = input("Nível do Pokémon: ")
            nivel_convertido = obter_nivel_pokemon(nivel)
            if isinstance(nivel_convertido, int):
                print(adicionar_pokemon(pokedex, nome, tipo, nivel_convertido))
            else:
                print(nivel_convertido)

        # 2. Listar Pokémon
        elif opcao == '2':
            print(listar_pokemon(pokedex))

        # 3. Remover Pokémon
        elif opcao == '3':
            nome = input("Nome do Pokémon a ser removido: ")
            print(remover_pokemon(pokedex, nome))

        # 4. Atualizar nível do Pokémon
        elif opcao == '4':
            nome = input("Nome do Pokémon a ser atualizado: ")
            nivel = input("Nível do Pokémon: ")
            nivel_convertido = obter_nivel_pokemon(nivel)
            if isinstance(nivel_convertido, int):
                print(atualizar_nivel_pokemon(pokedex, nome, nivel_convertido))
            else:
                print(nivel_convertido)

        # 5. Registrar captura de Pokémon
        elif opcao == '5':
            nome = input("Nome do Pokémon a ser registrado: ")
            try:
                capturas = int(input("Quantidade de capturas: "))
                print(registrar_captura(pokedex, historico_capturas, nome, capturas))
            except ValueError:
                print("Quantidade de capturas deve ser um número inteiro")

        # 6. Exibir histórico de capturas
        elif opcao == '6':
            print(exibir_historico_capturas(historico_capturas))

        elif opcao == '7':
            print("Saindo do programa. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()