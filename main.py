import mysql.connector
from faker import Faker

import mysql.connector
import time
import psutil
import os


# Configurações do MySQL
config = {
  'user': 'root',
  'password': '12345opi',
  'host': 'localhost',
  'database': 'vendas_db'
}

# Conectar ao MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

fake = Faker()

# Função para inserir dados fictícios na tabela de vendas
def insert_sales(n):
    cursor.execute("SELECT ClienteID FROM clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT FuncionarioID FROM funcionarios")
    funcionarios = cursor.fetchall()
    cursor.execute("SELECT ProdutoID FROM produtos")
    produtos = cursor.fetchall()

    for _ in range(n):
        cliente_id = fake.random_element(clientes)[0]
        funcionario_id = fake.random_element(funcionarios)[0]
        data_venda = fake.date_this_year()
        cursor.execute("INSERT INTO vendas (ClienteID, FuncionarioID, DataVenda) VALUES (%s, %s, %s)", (cliente_id, funcionario_id, data_venda))
        venda_id = cursor.lastrowid

        num_itens = fake.random_int(min=1, max=5)
        for _ in range(num_itens):
            produto_id = fake.random_element(produtos)[0]
            quantidade = fake.random_int(min=1, max=10)
            preco_venda = round(fake.random_number(digits=2), 2)
            cursor.execute("INSERT INTO itens_da_venda (VendaID, ProdutoID, Quantidade, PrecoVenda) VALUES (%s, %s, %s, %s)", (venda_id, produto_id, quantidade, preco_venda))
    conn.commit()

# Inserir dados
insert_sales(5000)

cursor.close()
conn.close()

cursor.close()
conn.close()
