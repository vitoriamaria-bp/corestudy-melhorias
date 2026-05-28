
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_core_study1"
        )

        return conexao

    except Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None