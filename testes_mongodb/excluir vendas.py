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

# Excluir 10.000 registros de vendas
vendas_a_excluir = db.vendas.find().limit(10000)
venda_ids = [venda['_id'] for venda in vendas_a_excluir]
result = db.vendas.delete_many({'_id': {'$in': venda_ids}})

# Medir tempo de execução
end_time = time.time()

# Medir recursos após a execução do código
measure_process_resources(process)

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")
print(f"Total de vendas excluídas: {result.deleted_count}")

client.close()
