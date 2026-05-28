import getpass
from conexao import conectar

def logar_sistema():
    print("\n--- TELA DE ACESSO ---")
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ")
    
    if email == "admin" and senha == "admin":
        return "ADMIN", "Administrador", 0

    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_usuario, nome_usuario FROM tbl_usuarios WHERE email_usuario = %s AND senha_usuario = %s", (email, senha))
        user = cursor.fetchone()
        cursor.close()
        conexao.close()
        if user: 
            return "ALUNO", user[1], user[0]
            
    print("\n[ERRO] E-mail ou senha incorretos.")
    return None, None, None