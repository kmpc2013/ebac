tarefas = {}

def adicionar_tarefa(nome):
    nome = nome

    if nome in tarefas:
        return "Essa tarefa já existe."
    else:
        tarefas[nome] = False
        return f"Tarefa '{nome}' adicionada com sucesso!!"

def listar_tarefas():
    if not tarefas:
        return "Nenhuma tarefa cadastrada."
    else:
        resultado = []

        for tarefa_nome, tarefa_status in sorted(tarefas.items(), key=lambda x: x[0]):
            status = "✅ Concluída" if tarefa_status else "❌ Não concluída"
            resultado.append(f"{tarefa_nome}: {status}")

        return "\n".join(resultado)


def remover_tarefa(nome):
    nome = nome

    if nome in tarefas:
        del tarefas[nome]
        return f"Tarefa '{nome}' removida com sucesso!"
    else:
        return "Erro: Tarefa não encontrada."


def marcar_concluida(nome):
    nome = nome

    if nome in tarefas:
        tarefas[nome] = True
        return f"Tarefa '{nome}' marcada como concluída!"
    else:
        return "Erro: Tarefa não encontrada."


def exibir_menu():
    print("\nMenu:")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Remover tarefa")
    print("4. Marcar tarefa como concluída")
    print("5. Sair")


def main():
    

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome da tarefa? ")
            print(adicionar_tarefa(nome))

        elif opcao == "2":
            print(listar_tarefas())

        elif opcao == "3":
            nome = input("Qual a tarefa a ser removida? ")
            print(remover_tarefa(nome))

        elif opcao == "4":
            nome = input("Qual a tarefa a ser marcada como concluída? ")
            print(marcar_concluida(nome))

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()