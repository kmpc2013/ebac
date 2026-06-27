def ler_texto_obrigatorio(prompt):
    valor = input(prompt).strip()
    if not valor:
        print("Entrada inválida. Por favor, informe um texto não vazio.")
        return None
    return valor


def ler_inteiro(prompt, permitir_zero=True):
    try:
        valor = int(input(prompt).strip())
        if permitir_zero:
            if valor < 0:
                raise ValueError
        else:
            if valor <= 0:
                raise ValueError
        return valor
    except ValueError:
        minimo = "0 ou maior" if permitir_zero else "maior que zero"
        print(f"Quantidade inválida. Informe um número inteiro {minimo}.")
        return None


def adicionar_livro(livros):
    titulo = ler_texto_obrigatorio("Título do livro: ")
    if titulo is None:
        return

    if titulo in livros:
        print(f"O livro '{titulo}' já existe no catálogo.")
        resposta = input("Deseja atualizar o autor e a quantidade? (s/n): ").strip().lower()
        if resposta not in ("s", "sim"):
            print("Nenhuma alteração foi feita no livro existente.")
            return

    autor = ler_texto_obrigatorio("Autor do livro: ")
    if autor is None:
        return

    quantidade = ler_inteiro("Quantidade de exemplares: ")
    if quantidade is None:
        return

    livro_existente = titulo in livros
    livros[titulo] = {"autor": autor, "quantidade": quantidade}
    acao = "atualizado" if livro_existente else "adicionado"
    print(f"Livro '{titulo}' {acao} com sucesso.")


def listar_livros(livros):
    if not livros:
        print("Nenhum livro cadastrado.")
        return

    print("Livros cadastrados:")
    linhas = [
        f"- {titulo} - {livros[titulo]['autor']} - {livros[titulo]['quantidade']} disponível(is)"
        for titulo in sorted(livros)
    ]
    print("\n".join(linhas))


def remover_livro(livros):
    titulo = ler_texto_obrigatorio("Título do livro a remover: ")
    if titulo is None:
        return

    if titulo in livros:
        del livros[titulo]
        print(f"Livro '{titulo}' removido com sucesso.")
    else:
        print(f"Erro: o livro '{titulo}' não existe.")


def atualizar_quantidade(livros):
    titulo = ler_texto_obrigatorio("Título do livro: ")
    if titulo is None:
        return

    if titulo not in livros:
        print(f"Erro: o livro '{titulo}' não existe.")
        return

    nova_quantidade = ler_inteiro("Nova quantidade de exemplares: ")
    if nova_quantidade is None:
        return

    livros[titulo]["quantidade"] = nova_quantidade
    print(f"Quantidade do livro '{titulo}' atualizada para {nova_quantidade}.")


def registrar_emprestimo(livros, historico):
    titulo = ler_texto_obrigatorio("Título do livro a emprestar: ")
    if titulo is None:
        return

    if titulo not in livros:
        print(f"Erro: o livro '{titulo}' não existe.")
        return

    quantidade_emprestada = ler_inteiro("Quantidade de exemplares para empréstimo: ", permitir_zero=False)
    if quantidade_emprestada is None:
        return

    disponivel = livros[titulo]["quantidade"]
    if quantidade_emprestada > disponivel:
        print(f"Erro: não há exemplares suficientes. Disponível: {disponivel}.")
        return

    livros[titulo]["quantidade"] = disponivel - quantidade_emprestada
    historico.append((titulo, quantidade_emprestada))
    print(f"Empréstimo registrado: {quantidade_emprestada} exemplar(es) de '{titulo}'.")


def exibir_historico_emprestimos(historico):
    if not historico:
        print("Nenhum empréstimo registrado.")
        return

    print("Histórico de empréstimos:")
    linhas = [
        f"{idx}. {titulo} - {quantidade} exemplar(es)"
        for idx, (titulo, quantidade) in enumerate(historico, start=1)
    ]
    print("\n".join(linhas))


def mostrar_menu():
    print("\n== Gerenciador de Biblioteca ==")
    opcoes = [
        "1. Adicionar livro",
        "2. Listar livros",
        "3. Remover livro",
        "4. Atualizar quantidade de livros",
        "5. Registrar empréstimo",
        "6. Exibir histórico de empréstimos",
        "7. Sair",
    ]
    print("\n".join(opcoes))


def main():
    livros = {}
    historico = []

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_livro(livros)
        elif opcao == "2":
            listar_livros(livros)
        elif opcao == "3":
            remover_livro(livros)
        elif opcao == "4":
            atualizar_quantidade(livros)
        elif opcao == "5":
            registrar_emprestimo(livros, historico)
        elif opcao == "6":
            exibir_historico_emprestimos(historico)
        elif opcao == "7":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
