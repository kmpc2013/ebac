def soma(a, b):
    print("O resultado é:", a + b)

def subtracao(a, b):
    print("O resultado é:", a - b)

def multiplicacao(a, b):
    print("O resultado é:", a * b)

def divisao(a, b):
    while b == 0:
        b = float(input("Divisão por zero não é permitida. Por favor, insira outro número: "))
    else:
        print("O resultado é:", a / b)

def menu():
    menu = [soma, subtracao, multiplicacao, divisao]
    menu_normalized = [f"{operacao} - {func.__name__}" for operacao, func in enumerate(menu, start=1)]
    return menu, menu_normalized

def main():
    print("================================")
    print("Bem-vindo à calculadora!")
    print("================================")


    continuar = True
    while continuar:
 
        # Função escolhida
        while True:
            try:
                num1 = float(input("Insira o primeiro número: "))
                break
            except ValueError:
                print("Digite apenas números.")
                continue
        while True:
            try:
                num2 = float(input("Insira o segundo número: "))
                break
            except ValueError:
                print("Digite apenas números.")
                continue
        
        # Menu de operações
        menu_func, menu_normalized = menu()
        print("\Escolha uma operação:")
        for item in menu_normalized:
            print(item)
        try:
            opcao = int(input("Digite a operação: "))
            if opcao < 1 or opcao > len(menu_func):
                print("Opção inválida!")
                continue
        except ValueError:
            print("Digite apenas números.")
            continue
        print(f"Você escolheu: {menu_func[int(opcao) - 1].__name__}.")
        
        menu_func[int(opcao) - 1](num1, num2)

        # Pergunta para continuar
        resposta = ""
        while resposta not in ["s", "n"]:
            resposta = input("\nDeseja realizar outra operação? (S/N): ").lower()
            if resposta not in ["s", "n"]:
                print("Resposta inválida. Por favor, digite 'S' para sim ou 'N' para não.")
        continuar = resposta == "s"

if __name__ == "__main__":
    main()