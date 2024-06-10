from pymongo import MongoClient
import psutil
import os
import time
from faker import Faker
from datetime import datetime

# Configuração MongoDB
url = 'mongodb://127.0.0.1:27017'
dbName = 'sistema_vendas'

# Função para medir a utilização de CPU e memória do processo atual
def measure_process_resources(process):
    cpu_usage = process.cpu_percent(interval=1)
    memory_info = process.memory_info()
    print(f"Uso de CPU do processo: {cpu_usage}%")
    print(f"Uso de Memória do processo: {memory_info.rss / 1024 / 1024} MB")  # Converte bytes para MB

# Obter o objeto do processo atual
process = psutil.Process(os.getpid())

# Criar uma instância do Faker
fake = Faker()

# Conectar ao MongoDB
client = MongoClient(url)
db = client[dbName]

# Medir recursos antes da execução do código
measure_process_resources(process)

# Medir tempo de execução
start_time = time.time()

# Inserir clientes
clientes = db.clientes
for _ in range(1000):
    cliente = {
        "nome": fake.name(),
        "email": fake.email(),
        "telefone": fake.phone_number()
    }
    clientes.insert_one(cliente)

# Inserir funcionários
funcionarios = db.funcionarios
for _ in range(100):
    funcionario = {
        "nome": fake.name(),
        "cargo": fake.job()
    }
    funcionarios.insert_one(funcionario)

# Inserir produtos
produtos = db.produtos
for _ in range(1000):
    produto = {
        "nome": fake.word(),
        "preco": float(fake.random_number(digits=2)),
        "quantidadeEstoque": fake.random_number(digits=3)
    }
    produtos.insert_one(produto)

# Recuperar todos os clientes, funcionários e produtos
clientes_list = list(clientes.find())
funcionarios_list = list(funcionarios.find())
produtos_list = list(produtos.find())

# Inserir vendas
vendas = db.vendas
for _ in range(50000):
    venda = {
        "cliente": fake.random_element(clientes_list),
        "funcionario": fake.random_element(funcionarios_list),
        "dataVenda": datetime.combine(fake.date_this_year(), datetime.min.time()),
        "itensVenda": []
    }
    num_itens = fake.random_int(min=1, max=5)
    for _ in range(num_itens):
        produto = fake.random_element(produtos_list)
        venda["itensVenda"].append({
            "produto": {
                "nome": produto["nome"],
                "preco": produto["preco"]
            },
            "quantidade": fake.random_int(min=1, max=10),
            "precoVenda": produto["preco"]
        })
    vendas.insert_one(venda)

# Medir tempo de execução
end_time = time.time()

# Medir recursos após a execução do código
measure_process_resources(process)

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")

client.close()
