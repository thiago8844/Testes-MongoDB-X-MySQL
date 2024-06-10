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

# Medir tempo de consulta de dados
start_time = time.time()

# Executar a consulta complexa com várias junções
query = """
SELECT 
    v.VendaID,
    v.DataVenda,
    c.nome AS ClienteNome,
    c.email AS ClienteEmail,
    c.telefone AS ClienteTelefone,
    f.nome AS FuncionarioNome,
    f.cargo AS FuncionarioCargo,
    p.nome AS ProdutoNome,
    p.preco AS ProdutoPreco,
    iv.Quantidade,
    iv.PrecoVenda
FROM vendas v
JOIN clientes c ON v.ClienteID = c.ClienteID
JOIN funcionarios f ON v.FuncionarioID = f.FuncionarioID
JOIN itens_da_venda iv ON v.VendaID = iv.VendaID
JOIN produtos p ON iv.ProdutoID = p.ProdutoID
"""

cursor.execute(query)
results = cursor.fetchall()

end_time = time.time()

# Medir recursos após a execução do código
measure_process_resources(process)

execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")

cursor.close()
conn.close()
