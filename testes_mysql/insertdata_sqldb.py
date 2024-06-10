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

# Função para medir a utilização de CPU e memória do processo atual
def measure_process_resources(process):
    cpu_usage = process.cpu_percent(interval=1)
    memory_info = process.memory_info()
    print(f"Uso de CPU do processo: {cpu_usage}%")
    print(f"Uso de Memória do processo: {memory_info.rss / 1024 / 1024} MB")  # Converte bytes para MB

# Obter o objeto do processo atual
process = psutil.Process(os.getpid())


# Conectar ao MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

fake = Faker()


# Medir recursos antes da execução do código
measure_process_resources(process)

# Medir tempo de consulta de dados
start_time = time.time()

# Função para inserir dados fictícios na tabela de produtos
def insert_products(n):
    for _ in range(n):
        nome = fake.word()
        preco = round(fake.random_number(digits=2), 2)
        quantidade = fake.random_number(digits=3)
        cursor.execute("INSERT INTO produtos (nome, preco, quantidadeEstoque) VALUES (%s, %s, %s)", (nome, preco, quantidade))
    conn.commit()

# Função para inserir dados fictícios na tabela de clientes
def insert_clients(n):
    for _ in range(n):
        nome = fake.name()
        email = fake.email()
        telefone = fake.phone_number()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)", (nome, email, telefone))
    conn.commit()

# Função para inserir dados fictícios na tabela de funcionários
def insert_employees(n):
    for _ in range(n):
        nome = fake.name()
        cargo = fake.job()
        cursor.execute("INSERT INTO funcionarios (nome, cargo) VALUES (%s, %s)", (nome, cargo))
    conn.commit()

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
insert_products(1000)
insert_clients(1000)
insert_employees(100)
insert_sales(50000)

end_time = time.time()
# Medir recursos após a execução do código
measure_process_resources(process)


execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")

cursor.close()
conn.close()

cursor.close()
conn.close()
