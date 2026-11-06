import sqlite3 as sql
import matplotlib.pyplot as plt

NOME_BANCO = "venda.db"
ANO_RELATORIO = "2023"

NOMES_MESES = {
    "01": "Jan", "02": "Fev", "03": "Mar",
    "04": "Abr", "05": "Mai", "06": "Jun",
    "07": "Jul", "08": "Ago", "09": "Set",
    "10": "Out", "11": "Nov", "12": "Dez",
}

VENDAS_INICIAIS = [
    ("2023-01-01", "Produto A", "Eletrônicos", 1500.00),
    ("2023-01-05", "Produto B", "Roupas", 350.00),
    ("2023-02-10", "Produto C", "Eletrônicos", 1200.00),
    ("2023-03-15", "Produto D", "Livros", 200.00),
    ("2023-03-20", "Produto E", "Eletrônicos", 800.00),
    ("2023-04-02", "Produto F", "Roupas", 400.00),
    ("2023-05-05", "Produto G", "Livros", 150.00),
    ("2023-06-10", "Produto H", "Eletrônicos", 1000.00),
    ("2023-07-20", "Produto I", "Roupas", 600.00),
    ("2023-08-25", "Produto J", "Eletrônicos", 700.00),
    ("2023-09-30", "Produto K", "Livros", 300.00),
    ("2023-10-05", "Produto L", "Roupas", 450.00),
    ("2023-11-15", "Produto M", "Eletrônicos", 900.00),
    ("2023-12-20", "Produto N", "Livros", 250.00),
]


# ---------------------------------------------------------------
# BANCO DE DADOS
# ---------------------------------------------------------------
def conectar():
    """Abre a conexão com o banco e devolve (conexao, cursor)."""
    conexao = sql.connect(NOME_BANCO)
    return conexao, conexao.cursor()


def criar_tabela(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas1 (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda DATE,
            produto TEXT,
            categoria TEXT,
            valor_venda REAL
        )
    """)


def inserir_dados(conexao, cursor):
    """Insere os dados iniciais apenas se a tabela estiver vazia."""
    cursor.execute("SELECT COUNT(*) FROM vendas1")
    if cursor.fetchone()[0] > 0:
        return

    cursor.executemany("""
        INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda)
        VALUES (?, ?, ?, ?)
    """, VENDAS_INICIAIS)
    conexao.commit()


def buscar_vendas(cursor):
    """Retorna as listas de datas, produtos, categorias, valores e o total de vendas."""
    cursor.execute("""
        SELECT data_venda, produto, categoria, valor_venda
        FROM vendas1
    """)
    dados = cursor.fetchall()

    datas = [linha[0] for linha in dados]
    produtos = [linha[1] for linha in dados]
    categorias = [linha[2] for linha in dados]
    valores = [linha[3] for linha in dados]

    return datas, produtos, categorias, valores, len(dados)


# ---------------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------------
def grafico_de_setores(categorias):
    """Gráfico de pizza com a quantidade de vendas por categoria."""
    nomes = ["Eletrônicos", "Roupas", "Livros"]
    quantidades = [categorias.count(nome) for nome in nomes]

    plt.figure(figsize=(7, 5))
    plt.pie(quantidades, labels=nomes, autopct="%1.1f%%")
    plt.title("Vendas por categoria")
    plt.show()


def grafico_faturamento_mensal(meses, valores):
    """Gráfico de barras com o faturamento de cada mês."""
    plt.figure(figsize=(10, 5))
    plt.bar(meses, valores)
    plt.title(f"Faturamento mensal de {ANO_RELATORIO}")
    plt.ylabel("Total vendido (R$)")
    plt.xlabel("Meses")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------
# RELATÓRIO
# ---------------------------------------------------------------
def relatorio_anual(cursor):
    """Imprime o relatório geral do ano e mostra o gráfico mensal."""
    cursor.execute("""
        SELECT COUNT(*), SUM(valor_venda), AVG(valor_venda)
        FROM vendas1
        WHERE strftime('%Y', data_venda) = ?
    """, (ANO_RELATORIO,))
    total_vendas, faturamento, ticket_medio = cursor.fetchone()

    print(f"\n===== RELATÓRIO DE VENDAS DE {ANO_RELATORIO} =====")

    if total_vendas == 0:
        print(f"Nenhuma venda encontrada em {ANO_RELATORIO}.")
        return

    print(f"Quantidade de vendas: {total_vendas}")
    print(f"Faturamento total: R$ {faturamento:.2f}")
    print(f"Ticket médio: R$ {ticket_medio:.2f}")

    # Faturamento por mês
    cursor.execute("""
        SELECT strftime('%m', data_venda) AS mes, SUM(valor_venda) AS total
        FROM vendas1
        WHERE strftime('%Y', data_venda) = ?
        GROUP BY mes
        ORDER BY mes
    """, (ANO_RELATORIO,))
    dados = cursor.fetchall()

    if not dados:
        print("Não existem valores mensais para mostrar.")
        return

    meses = [NOMES_MESES[linha[0]] for linha in dados]
    valores = [linha[1] for linha in dados]

    indice_maior = valores.index(max(valores))
    indice_menor = valores.index(min(valores))

    print(f"Melhor mês: {meses[indice_maior]} - R$ {valores[indice_maior]:.2f}")
    print(f"Pior mês: {meses[indice_menor]} - R$ {valores[indice_menor]:.2f}")

    grafico_faturamento_mensal(meses, valores)


# ---------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
def main():
    conexao, cursor = conectar()

    try:
        criar_tabela(cursor)
        inserir_dados(conexao, cursor)

        _, _, categorias, _, total = buscar_vendas(cursor)
        print(f"Total de produtos cadastrados: {total}")

        grafico_de_setores(categorias)
        relatorio_anual(cursor)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
