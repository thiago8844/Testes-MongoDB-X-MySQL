import mysql.connector
import time
import psutil
import os

# Configuração MySQL
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

# Medir recursos antes da execução do código
measure_process_resources(process)

# Medir tempo de atualização de dados
start_time = time.time()

# Executar a atualização de dados
# Atualizar o campo 'DataVenda' para uma nova data para todos os registros
new_date = '2024-06-10'
cursor.execute("UPDATE vendas SET DataVenda = %s", (new_date,))

# Confirma a atualização
conn.commit()

end_time = time.time()

# Medir recursos após a execução do código
measure_process_resources(process)

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")

cursor.close()
conn.close()
