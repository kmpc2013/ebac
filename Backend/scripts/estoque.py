def adicionar_produto(estoque, nome, quantidade, preco):
    nome = nome.strip()
    if nome in estoque:
        return "Erro: Produto já cadastrado."
    else:
        estoque[nome] = {"quantidade": quantidade, "preco": preco}
        return f"Produto '{nome}' adicionado com sucesso!"

def listar_produtos(estoque):
    if not estoque:
        return "Nenhum produto cadastrado."
    else:
        resultado = []
        for nome, array in sorted(estoque.items(), key=lambda x: x[0]):
            resultado.append(f"{nome}: {array['quantidade']} - R${array['preco']:.2f}")
        return "\n".join(resultado)

def remover_produto(estoque, nome):
    nome = nome.strip()
    if nome in estoque:
        del estoque[nome]
        return f"Produto '{nome}' removido com sucesso!"
    else:
        return "Erro: Produto não encontrado."

def atualizar_quantidade(estoque, nome, quantidade):
    nome = nome.strip()
    if nome in estoque:
        estoque[nome]["quantidade"] = quantidade
        return f"Quantidade do produto '{nome}' atualizada para {quantidade}."
    else:
        return "Erro: Produto não encontrado."

def exibir_menu():
    return (
        "\nMenu:"
        "\n1 - Adicionar produto"
        "\n2 - Listar produtos"
        "\n3 - Remover produto"
        "\n4 - Atualizar quantidade"
        "\n5 - Sair"
    )

def main():
    estoque = {}
    while True:
        print(exibir_menu())
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do produto? ")
            quantidade = int(input("Quantidade? "))
            preco = float(input("Preço? "))
            print(adicionar_produto(estoque, nome, quantidade, preco))
        elif opcao == "2":
            print(listar_produtos(estoque))
        elif opcao == "3":
            nome = input("Nome do produto a ser removido? ")
            print(remover_produto(estoque, nome))
        elif opcao == "4":
            nome = input("Nome do produto a ter quantidade atualizada? ")
            nova_qtd = int(input("Nova quantidade? "))
            print(atualizar_quantidade(estoque, nome, nova_qtd))
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()