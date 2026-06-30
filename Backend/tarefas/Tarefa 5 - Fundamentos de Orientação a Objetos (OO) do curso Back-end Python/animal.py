class Animal:  # Definição da classe base Animal
    def __init__(self, nome, idade):  # Método construtor (__init__) que inicializa um objeto Animal
        self.nome = nome  # Atribui o valor do parâmetro ao atributo 'nome' do objeto
        self.idade = int(idade)  # Atribui o valor do parâmetro ao atributo 'idade' do objeto

    def emitir_som(self):  # Método para o animal emitir um som
        return "O animal emitiu um som genérico."  # Retorna uma string genérica para o som do animal

class Cachorro(Animal):  # Definição da classe Cachorro, que herda da classe Animal
    def emitir_som(self):  # Sobrescrita do método emitir_som para um comportamento específico de Cachorro
        return "O cachorro latiu!" # Retorna o som característico do cachorro

class Gato(Animal):  # Definição da classe Gato, que herda da classe Animal
    def emitir_som(self):  # Sobrescrita do método emitir_som para um comportamento específico de Gato
        return "O gato miou!"  # Retorna o som característico do gato
    
def main():
    cachorro = Cachorro("Rex", 5)  # Criação de um objeto Cachorro com nome "Rex" e idade 5
    gato = Gato("Mia", 3)  # Criação de um objeto Gato com nome "Mia" e idade 3

    print(f"{cachorro.nome} tem {cachorro.idade} anos e diz: {cachorro.emitir_som()}")  # Imprime as informações do cachorro e o som que ele emite
    print(f"{gato.nome} tem {gato.idade} anos e diz: {gato.emitir_som()}")  # Imprime as informações do gato e o som que ele emite


if __name__ == "__main__":
    main()  # Chama a função main para executar o programa