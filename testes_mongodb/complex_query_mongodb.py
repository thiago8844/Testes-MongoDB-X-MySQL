from pymongo import MongoClient
import psutil
import os
import time

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

# Conectar ao MongoDB
client = MongoClient(url)
db = client[dbName]

# Medir recursos antes da execução do código
measure_process_resources(process)

# Medir tempo de execução
start_time = time.time()

# Executar a consulta complexa com agregações
pipeline = [
    {
        '$lookup': {
            'from': 'clientes',
            'localField': 'cliente._id',
            'foreignField': '_id',
            'as': 'cliente_info'
        }
    },
    {
        '$unwind': {
            'path': '$cliente_info',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$lookup': {
            'from': 'funcionarios',
            'localField': 'funcionario._id',
            'foreignField': '_id',
            'as': 'funcionario_info'
        }
    },
    {
        '$unwind': {
            'path': '$funcionario_info',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$unwind': {
            'path': '$itensVenda',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$lookup': {
            'from': 'produtos',
            'localField': 'itensVenda.produto._id',
            'foreignField': '_id',
            'as': 'produto_detalhes'
        }
    },
    {
        '$unwind': {
            'path': '$produto_detalhes',
            'preserveNullAndEmptyArrays': True
        }
    }
]
vendas_detalhadas = db.vendas.aggregate(pipeline)
vendas_detalhadas_list = list(vendas_detalhadas)

# Medir tempo de execução
end_time = time.time()

# Medir recursos após a execução do código
measure_process_resources(process)

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")
print(f"Total de vendas detalhadas consultadas: {len(vendas_detalhadas_list)}")

client.close()
