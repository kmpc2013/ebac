def obter_dados_livro(titulo, autor, quantidade):
    return f"{titulo} {autor} {quantidade}"


def obter_quantidade_livro(valor):
    try:
        quantidade = int(valor)
        if quantidade < 0:
            return "Por favor, insira um número válido para a quantidade."
        return quantidade
    except ValueError:
        return "Por favor, insira um número válido para a quantidade."


def validar_livro_existe(livros, titulo):
    if titulo in livros:
        return True
    return f"Erro: O livro '{titulo}' não foi encontrado."


def adicionar_livro(livros, titulo, autor, quantidade):
    if validar_livro_existe(livros, titulo) is True:
        return f"Erro: o livro '{titulo}' já existe no catálogo."
    livros[titulo] = {"autor": autor, "quantidade": quantidade}
    return f"Livro '{titulo}' adicionado com sucesso"


def listar_livros(livros):
    if not livros:
        return 'Não há livros cadastrados.'
    linhas = [
        f"- {titulo} - {dados['autor']} - {dados['quantidade']} disponível(is)"
        for titulo, dados in sorted(livros.items())
    ]
    return "\n".join(linhas)


def remover_livro(livros, titulo):
    if validar_livro_existe(livros, titulo) is True:
        del livros[titulo]
        return f"Livro '{titulo}' removido com sucesso!"
    else:
        return f'Erro: Livro "{titulo}" não encontrado.'


def atualizar_quantidade(livros, titulo, quantidade):
    if validar_livro_existe(livros, titulo) is True:
        livros[titulo] = livros.get(titulo, {})
        livros[titulo]["quantidade"] = quantidade
        return f"Quantidade de exemplares do livro '{titulo}' atualizada para {quantidade}"
    else:
        return f"Erro: O livro '{titulo}' não foi encontrado."


def registrar_emprestimo(livros, historico, titulo, quantidade):
    if validar_livro_existe(livros, titulo) is True:
        if livros[titulo].get("quantidade", 0) >= quantidade:
            livros[titulo]["quantidade"] -= quantidade
            historico.append((titulo, quantidade))
            return f"{quantidade} exemplares de '{titulo}' emprestados com sucesso!"
        else:
            return "Erro: Não há livros suficientes disponíveis."
    else:
        return f"Erro: O livro '{titulo}' não foi encontrado."


def obter_quantidade_livro_para_emprestimo(biblioteca, titulo, quantidade):
    try:
        qtd = int(quantidade)
        if qtd <= 0:
            return "Por favor, insira um número válido para a quantidade."
        elif qtd > biblioteca.get(titulo, {}).get("quantidade", 0):
            return "Erro: Não há livros suficientes disponíveis."
        else:
            return qtd
    except (ValueError, TypeError):
        return "Por favor, insira um número válido para a quantidade."


def exibir_historico_emprestimos(historico):
    if not historico:
        return "Não há histórico de empréstimos."
    return "\n".join([
        f"{idx}. {titulo} - {quantidade} exemplar(es)"
        for idx, (titulo, quantidade) in enumerate(historico, start=1)
    ])


def exibir_menu():
    return (
        "\n== Gerenciador de Biblioteca ==\n"
        "1. Adicionar livro\n"
        "2. Listar livros\n"
        "3. Remover livro\n"
        "4. Atualizar quantidade de livros\n"
        "5. Registrar empréstimo\n"
        "6. Exibir histórico de empréstimos\n"
        "7. Sair"
    )


def main():
    livros = {}
    historico = []

    while True:
        print(exibir_menu())
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título do livro: ").strip()
            autor = input("Autor do livro: ").strip()
            quantidade = obter_quantidade_livro(input("Quantidade de exemplares: ").strip())
            if titulo and autor and isinstance(quantidade, int):
                result = adicionar_livro(livros, titulo, autor, quantidade)
                print(result)
            else:
                if isinstance(quantidade, str):
                    print(quantidade)
                else:
                    print("Dados inválidos. Tente novamente.")
        elif opcao == "2":
            livros_cadastrados = listar_livros(livros)
            if livros_cadastrados:
                print("Livros cadastrados:")
                print(livros_cadastrados)
            else:
                print('Não há livros cadastrados.')
        elif opcao == "3":
            titulo = input("Título do livro a remover: ").strip()
            result = remover_livro(livros, titulo)
            print(result)
        elif opcao == "4":
            titulo = input("Título do livro: ").strip()
            quantidade = obter_quantidade_livro(input("Nova quantidade de exemplares: ").strip())
            if isinstance(quantidade, int):
                result = atualizar_quantidade(livros, titulo, quantidade)
                print(result)
            else:
                print(quantidade)
        elif opcao == "5":
            titulo = input("Título do livro a emprestar: ").strip()
            quantidade_emprestada = input("Quantidade de exemplares para empréstimo: ").strip()
            quantidade_valida = obter_quantidade_livro_para_emprestimo(livros, titulo, quantidade_emprestada)
            if isinstance(quantidade_valida, int):
                result = registrar_emprestimo(livros, historico, titulo, quantidade_valida)
                print(result)
            else:
                print(quantidade_valida)
        elif opcao == "6":
            historico_texto = exibir_historico_emprestimos(historico)
            if historico:
                print("Histórico de empréstimos:")
                print(historico_texto)
            else:
                print(historico_texto)
        elif opcao == "7":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
