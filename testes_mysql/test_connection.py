import mysql.connector
from mysql.connector import Error

def test_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # substitua 'seu_usuario' pelo seu nome de usuário do MySQL
            password='12345opi',      # substitua 'sua_senha' pela sua senha do MySQL
            database='vendas_db'  # substitua 'sistema_vendas' pelo nome do seu banco de dados
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Conectado ao MySQL Server versão ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Conectado ao banco de dados: ", record)
    except Error as e:
        print("Erro ao conectar ao MySQL", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão ao MySQL foi fechada")

test_connection()