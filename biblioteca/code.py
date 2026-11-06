# Classe que representa um livro
class Livro:
    def __init__(self, titulo, autor, genero, quantidade):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.quantidade = quantidade
 
 
# Cadastra um novo livro
def cadastro():
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    genero = input("Digite o gênero do livro: ")
    quantidade = int(input("Digite a quantidade disponível: "))
 
    return titulo, autor, genero, quantidade
 
 
# Lista todos os livros cadastrados
def listar_livros():
    for livro in livros:
        print(f"\nTítulo: {livro.titulo}")
        print(f"Autor: {livro.autor}")
        print(f"Gênero: {livro.genero}")
        print(f"Quantidade: {livro.quantidade}")
        print("--------------------")
 
 
# Busca um livro pelo título
def buscar_livro():
    titulo_busca = input("Digite o título do livro que deseja buscar: ")
 
    # Percorre a lista procurando o título
    for livro in livros:
        if livro.titulo.lower() == titulo_busca.lower():
            print(f"\nTítulo: {livro.titulo}")
            print(f"Autor: {livro.autor}")
            print(f"Gênero: {livro.genero}")
            print(f"Quantidade: {livro.quantidade}")
            return
 
    print("Livro não encontrado.")
 
 
# Cria um gráfico com os gêneros dos livros
def grafico_generos():
    generos = {}
 
    # Conta quantos livros existem por gênero
    for livro in livros:
        if livro.genero in generos:
            generos[livro.genero] += 1
        else:
            generos[livro.genero] = 1
 
    # Cria e exibe o gráfico
    plt.bar(generos.keys(), generos.values())
    plt.xlabel("Gênero")
    plt.ylabel("Quantidade de livros")
    plt.title("Quantidade de livros por gênero")
    plt.show()
 
 
# Lista que armazena os livros
livros = []
 
 
# Repete o programa até o cadastro ser concluído
while True:
    try:
        pergunta = int(input("Quantos livros você gostaria de adicionar? "))
 
        if pergunta <= 0:
            print("Digite um número maior que 0")
 
        else:
            # Cadastra a quantidade de livros escolhida
            for i in range(pergunta):
                print(f"\nCadastro do livro {i + 1}")
 
                titulo, autor, genero, quantidade = cadastro()
 
                # Cria o objeto Livro
                cadastro_de_livro = Livro(titulo, autor, genero, quantidade)
 
                # Adiciona o livro na lista
                livros.append(cadastro_de_livro)
 
            listar_livros()
            buscar_livro()
            grafico_generos()
 
            # Encerra o programa
            break
 
    # Evita erro quando o usuário não digita um número
    except ValueError:
        print("Digite apenas um número.")
