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
    except Error as error:
        print(f"Erro ao conectar no MySQL: {error}")
        return None

def criar_tabelas():
    conexao = conectar()
    if conexao is None: return
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_usuarios (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nome_usuario VARCHAR(100) NOT NULL, email_usuario VARCHAR(200) NOT NULL, telefone_usuario VARCHAR(50) NOT NULL, dt_nasc_usuario DATE NOT NULL, senha_usuario VARCHAR(100) NOT NULL, dt_cad_usuario DATE DEFAULT (CURRENT_DATE))")
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_categoria (id_categoria INT AUTO_INCREMENT PRIMARY KEY, nome_categoria VARCHAR(100) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_cursos (id_curso INT AUTO_INCREMENT PRIMARY KEY, titulo_curso VARCHAR(100) NOT NULL, descricao_curso VARCHAR(500) NOT NULL, carga_hora_curso INT NOT NULL, fk_tbl_categoria_id_categoria INT NOT NULL, CONSTRAINT FK_tbl_cursos_categoria FOREIGN KEY (fk_tbl_categoria_id_categoria) REFERENCES tbl_categoria(id_categoria) ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_modulos (id_modulo INT AUTO_INCREMENT PRIMARY KEY, titulo_modulo VARCHAR(100) NOT NULL, fk_tbl_cursos_id_curso INT NOT NULL, CONSTRAINT FK_tbl_modulos_cursos FOREIGN KEY (fk_tbl_cursos_id_curso) REFERENCES tbl_cursos(id_curso) ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_aulas (id_aula INT AUTO_INCREMENT PRIMARY KEY, titulo_aula VARCHAR(200) NOT NULL, url_arqui_aula VARCHAR(2000) NOT NULL, fk_tbl_modulos_id_modulo INT NOT NULL, CONSTRAINT FK_tbl_aulas_modulos FOREIGN KEY (fk_tbl_modulos_id_modulo) REFERENCES tbl_modulos(id_modulo) ON DELETE RESTRICT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_materiais (id_material INT AUTO_INCREMENT PRIMARY KEY, nome_material VARCHAR(200) NOT NULL, tipo_material VARCHAR(100), tam_arqu_material VARCHAR(200), fk_tbl_aulas_id_aula INT NOT NULL, CONSTRAINT FK_tbl_materiais_aulas FOREIGN KEY (fk_tbl_aulas_id_aula) REFERENCES tbl_aulas(id_aula) ON DELETE CASCADE)")
    conexao.commit()
    cursor.close()
    conexao.close()