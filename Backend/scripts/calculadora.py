while True:
    print("Escolha a operação:")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")

    opcao = input("Digite o número da operação desejada: ")
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))

    if opcao == "1":
        print("Resultado:", num1 + num2)
    # Continue o código
    elif opcao == "2":
        print("Resultado:", num1 - num2)
    elif opcao == "3":
        print("Resultado:", num1 * num2)
    elif opcao == "4":
        if num1 == 0 or num2 == 0:
            print("zero")
        else:
            print("Resultado:", num1 / num2)
    else:
        print("inválido")
    
    resposta = input("\nDeseja realizar outra operação? (s/n): ").lower()
    if resposta != 's':
        print("Encerrando a calculadora. Até mais!")
        break