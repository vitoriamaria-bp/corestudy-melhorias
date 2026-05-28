import mysql.connector
from mysql.connector import Error
from mysql.connector import IntegrityError
import getpass


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

    if conexao is None:
        return

    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        nome_usuario VARCHAR(200) NOT NULL,
        email_usuario VARCHAR(200) NOT NULL,
        telefone_usuario VARCHAR(50) NOT NULL,
        dt_nasc_usuario DATE NOT NULL,
        senha_usuario VARCHAR(100) NOT NULL,
        dt_cad_usuario DATE DEFAULT (CURRENT_DATE)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_categoria (
        id_categoria INT AUTO_INCREMENT PRIMARY KEY,
        nome_categoria VARCHAR(100) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_cursos (
        id_curso INT AUTO_INCREMENT PRIMARY KEY,
        titulo_curso VARCHAR(100) NOT NULL,
        descricao_curso VARCHAR(500) NOT NULL,
        carga_hora_curso INT NOT NULL,
        fk_tbl_categoria_id_categoria INT NOT NULL,

        CONSTRAINT FK_tbl_cursos_categoria
            FOREIGN KEY (fk_tbl_categoria_id_categoria)
            REFERENCES tbl_categoria(id_categoria)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_modulos (
        id_modulo INT AUTO_INCREMENT PRIMARY KEY,
        titulo_modulo VARCHAR(100) NOT NULL,
        fk_tbl_cursos_id_curso INT NOT NULL,

        CONSTRAINT FK_tbl_modulos_cursos
            FOREIGN KEY (fk_tbl_cursos_id_curso)
            REFERENCES tbl_cursos(id_curso)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_aulas (
        id_aula INT AUTO_INCREMENT PRIMARY KEY,
        titulo_aula VARCHAR(200) NOT NULL,
        url_arqui_aula VARCHAR(2000) NOT NULL,
        fk_tbl_modulos_id_modulo INT NOT NULL,

        CONSTRAINT FK_tbl_aulas_modulos
            FOREIGN KEY (fk_tbl_modulos_id_modulo)
            REFERENCES tbl_modulos(id_modulo)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_materiais (
        id_material INT AUTO_INCREMENT PRIMARY KEY,
        nome_material VARCHAR(200) NOT NULL,
        tipo_material VARCHAR(100),
        tam_arqu_material VARCHAR(200),
        fk_tbl_aulas_id_aula INT NOT NULL,

        CONSTRAINT FK_tbl_materiais_aulas
            FOREIGN KEY (fk_tbl_aulas_id_aula)
            REFERENCES tbl_aulas(id_aula)
            ON DELETE CASCADE
    )
    """)

    conexao.commit()
    print("Tabelas criadas com sucesso!")

    cursor.close()
    conexao.close()


def adicionar_usuario():

    nome = input("Nome do usuário: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    dt_nasc = input("Data de nascimento (AAAA-MM-DD): ")
    senha = getpass.getpass("Senha: ")

    aceite = input("Aceita os termos de uso? (s/n): ")
    if aceite.upper() != "S":
        print("Cadastro cancelado!")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_usuarios
    (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario)
    VALUES (%s, %s, %s, %s, %s)
    """

    valores = (nome, email, telefone, dt_nasc, senha)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Usuário cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_usuarios")
    usuarios = cursor.fetchall()

    print("\n========= USUÁRIOS =========")

    for usuario in usuarios:
        print(f"ID: {usuario[0]}")
        print(f"Nome: {usuario[1]}")
        print(f"Email: {usuario[2]}")
        print(f"Telefone: {usuario[3]}")
        print(f"Nascimento: {usuario[4]}")
        print(f"Data cadastro: {usuario[6]}")
        print("-" * 40)

    cursor.close()
    conexao.close()


def atualizar_usuario():
    listar_usuarios()

    id_usuario = input("Digite o ID do usuário que deseja atualizar: ")
    nome = input("Novo nome: ")
    email = input("Novo email: ")
    telefone = input("Novo telefone: ")
    dt_nasc = input("Nova data de nascimento (AAAA-MM-DD): ")
    senha = getpass.getpass("Nova senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_usuarios
    SET nome_usuario = %s,
        email_usuario = %s,
        telefone_usuario = %s,
        dt_nasc_usuario = %s,
        senha_usuario = %s
    WHERE id_usuario = %s
    """

    valores = (nome, email, telefone, dt_nasc, senha, id_usuario)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Usuário atualizado com sucesso!")

    cursor.close()
    conexao.close()


def deletar_usuario():
    listar_usuarios()

    id_usuario = input("Digite o ID do usuário que deseja deletar: ")

    confirmar = input("Tem certeza que deseja deletar este usuário? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    DELETE FROM tbl_usuarios
    WHERE id_usuario = %s
    """

    try:
        cursor.execute(sql, (id_usuario,))
        conexao.commit()
        print("Usuário deletado com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir este usuário, pois existem dados vinculados a ele.")
    finally:
        cursor.close()
        conexao.close()


def logar_sistema():
    
    print("\n====== TELA DE ACESSO ======")
    email = input("Digite seu email: ")
    senha = getpass.getpass("Digite sua senha: ")

    if email == "admin" and senha == "admin":
        return "ADMIN", "Administrador", 0
    
    conexao = conectar()
    
    if conexao:
        cursor = conexao.cursor()

        sql = "SELECT id_usuario, nome_usuario FROM tbl_usuarios WHERE email_usuario = %s AND senha_usuario = %s"

        cursor.execute(sql, (email, senha))

        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if usuario:
            return "ALUNO", usuario[1], usuario [0]
        
    print("\n[ERRO] E-mail ou senha inválida!")
    return None, None, None


def adicionar_categoria():
    nome = input("Nome da categoria: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_categoria (nome_categoria)
    VALUES (%s)
    """

    cursor.execute(sql, (nome,))
    conexao.commit()

    print("Categoria cadastrada com sucesso!")

    cursor.close()
    conexao.close()


def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_categoria")
    categorias = cursor.fetchall()

    print("\n========= CATEGORIAS =========")
    for categoria in categorias:
        print(f"ID: {categoria[0]}")
        print(f"Nome: {categoria[1]}")
        print("-" * 30)

    cursor.close()
    conexao.close()


def editar_categoria():

    listar_categorias()

    id_categoria = input("Digite o ID da categoria: ")
    novo_nome = input("Novo nome da categoria: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE tbl_categoria SET nome_categoria = %s WHERE id_categoria = %s"

    cursor.execute(sql, (novo_nome, id_categoria))

    conexao.commit()

    print("Categoria atualizada com sucesso!")

    cursor.close()
    conexao.close()


def excluir_categoria():

    listar_categorias()

    id_categoria = input("Digite o ID da categoria: ")
    confirmar = input("Tem certeza que deseja excluir? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_categoria WHERE id_categoria = %s"

    try:
        cursor.execute(sql, (id_categoria,))
        conexao.commit()
        print("Categoria excluída com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir esta categoria, pois existem cursos vinculados a ela.")
    finally:
        cursor.close()
        conexao.close()


def adicionar_curso():
    titulo = input("Título do curso: ")
    descricao = input("Descrição do curso: ")
    carga_hora = int(input("Carga horária do curso: "))

    listar_categorias()
    categoria_id = int(input("Digite o ID da categoria: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO tbl_cursos (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria)" \
    " VALUES (%s, %s, %s, %s)"

    valores = (titulo, descricao, carga_hora, categoria_id)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Curso cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_cursos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_cursos.id_curso,
           tbl_cursos.titulo_curso,
           tbl_cursos.descricao_curso,
           tbl_cursos.carga_hora_curso,
           tbl_categoria.nome_categoria
    FROM tbl_cursos
    INNER JOIN tbl_categoria
    ON tbl_cursos.fk_tbl_categoria_id_categoria = tbl_categoria.id_categoria
    """

    cursor.execute(sql)
    cursos = cursor.fetchall()

    print("\n========= CURSOS =========")
    for curso in cursos:
        print(f"ID: {curso[0]}")
        print(f"Título: {curso[1]}")
        print(f"Descrição: {curso[2]}")
        print(f"Carga horária: {curso[3]} horas")
        print(f"Categoria: {curso[4]}")
        print("-" * 40)

    cursor.close()
    conexao.close()


def editar_curso():

    listar_cursos()

    id_curso = input("Digite o ID do curso: ")
    titulo = input("Novo título do curso: ")
    descricao = input("Nova descrição do curso: ")
    carga_hora = int(input("Nova carga horária: "))

    listar_categorias()
    categoria_id = int(input("Novo ID da categoria: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_cursos
    SET titulo_curso = %s,
        descricao_curso = %s,
        carga_hora_curso = %s,
        fk_tbl_categoria_id_categoria = %s
    WHERE id_curso = %s
    """

    cursor.execute(sql, (titulo, descricao, carga_hora, categoria_id, id_curso))
    conexao.commit()

    print("Curso atualizado com sucesso!")

    cursor.close()
    conexao.close()


def excluir_curso():

    listar_cursos()

    id_curso = input("Digite o ID do curso: ")

    confirmar = input("Tem certeza que deseja excluir este curso? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    DELETE FROM tbl_cursos
    WHERE id_curso = %s
    """

    try:
        cursor.execute(sql, (id_curso,))
        conexao.commit()
        print("Curso excluído com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir este curso, pois existem módulos vinculados a ele.")
    finally:
        cursor.close()
        conexao.close()


def adicionar_modulo():
    titulo = input("Título do módulo: ")

    listar_cursos()
    curso_id = int(input("Digite o ID do curso: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_modulos
    (titulo_modulo, fk_tbl_cursos_id_curso)
    VALUES (%s, %s)
    """

    cursor.execute(sql, (titulo, curso_id))
    conexao.commit()

    print("Módulo cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_modulos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_modulos.id_modulo,
           tbl_modulos.titulo_modulo,
           tbl_cursos.titulo_curso
    FROM tbl_modulos
    INNER JOIN tbl_cursos
    ON tbl_modulos.fk_tbl_cursos_id_curso = tbl_cursos.id_curso
    """

    cursor.execute(sql)
    modulos = cursor.fetchall()

    print("\n===== MÓDULOS =====")
    for modulo in modulos:
        print(f"ID: {modulo[0]}")
        print(f"Módulo: {modulo[1]}")
        print(f"Curso: {modulo[2]}")
        print("-" * 40)

    cursor.close()
    conexao.close()


def editar_modulo():

    listar_modulos()

    id_modulo = input("Digite o ID do módulo: ")
    titulo = input("Novo título do módulo: ")

    listar_cursos()
    curso_id = int(input("Novo ID do curso: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_modulos
    SET titulo_modulo = %s,
        fk_tbl_cursos_id_curso = %s
    WHERE id_modulo = %s
    """

    cursor.execute(sql, (titulo, curso_id, id_modulo))
    conexao.commit()

    print("Módulo atualizado com sucesso!")

    cursor.close()
    conexao.close()


def excluir_modulo():

    listar_modulos()

    id_modulo = input("Digite o ID do módulo: ")

    confirmar = input("Tem certeza que deseja excluir este módulo? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_modulos WHERE id_modulo = %s"

    try:
        cursor.execute(sql, (id_modulo,))
        conexao.commit()
        print("Módulo excluído com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir este módulo, pois existem aulas vinculadas a ele.")
    finally:
        cursor.close()
        conexao.close()


def adicionar_aula():
    titulo = input("Título da aula: ")
    url = input("URL/arquivo da aula: ")

    listar_modulos()
    modulo_id = int(input("Digite o ID do módulo: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_aulas
    (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (titulo, url, modulo_id))
    conexao.commit()

    print("Aula cadastrada com sucesso!")

    cursor.close()
    conexao.close()


def listar_aulas():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_aulas.id_aula,
           tbl_aulas.titulo_aula,
           tbl_aulas.url_arqui_aula,
           tbl_modulos.titulo_modulo,
           tbl_cursos.titulo_curso
    FROM tbl_aulas
    INNER JOIN tbl_modulos
    ON tbl_aulas.fk_tbl_modulos_id_modulo = tbl_modulos.id_modulo
    INNER JOIN tbl_cursos
    ON tbl_modulos.fk_tbl_cursos_id_curso = tbl_cursos.id_curso
    """

    cursor.execute(sql)
    aulas = cursor.fetchall()

    print("\n========= AULAS =========")
    for aula in aulas:

        print(f"ID: {aula[0]}")
        print(f"Aula: {aula[1]}")
        print(f"Arquivo/URL: {aula[2]}")
        print(f"Módulo: {aula[3]}")
        print(f"Curso: {aula[4]}")
        print("-" * 40)

    cursor.close()
    conexao.close()


def editar_aula():

    listar_aulas()

    id_aula = input("Digite o ID da aula: ")
    titulo = input("Novo título da aula: ")
    url = input("Nova URL/arquivo da aula: ")

    listar_modulos()
    modulo_id = int(input("Novo ID do módulo: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_aulas
    SET titulo_aula = %s,
        url_arqui_aula = %s,
        fk_tbl_modulos_id_modulo = %s
    WHERE id_aula = %s
    """

    cursor.execute(sql, (titulo, url, modulo_id, id_aula))
    conexao.commit()

    print("Aula atualizada com sucesso!")

    cursor.close()
    conexao.close()


def excluir_aula():

    listar_aulas()

    id_aula = input("Digite o ID da aula: ")
    confirmar = input("Tem certeza que deseja excluir esta aula? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_aulas WHERE id_aula = %s"

    try:
        cursor.execute(sql, (id_aula,))
        conexao.commit()
        print("Aula excluída com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir esta aula, pois existem materiais vinculados a ela.")
    finally:
        cursor.close()
        conexao.close()


def adicionar_material():
    nome = input("Nome do material: ")
    tipo = input("Tipo do material: ")
    tamanho = input("Tamanho do arquivo: ")

    listar_aulas()
    aula_id = int(input("Digite o ID da aula: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_materiais
    (nome_material, tipo_material, tam_arqu_material, fk_tbl_aulas_id_aula)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, tipo, tamanho, aula_id))
    conexao.commit()

    print("Material cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_materiais():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_materiais.id_material,
           tbl_materiais.nome_material,
           tbl_materiais.tipo_material,
           tbl_materiais.tam_arqu_material,
           tbl_aulas.titulo_aula
    FROM tbl_materiais
    INNER JOIN tbl_aulas
    ON tbl_materiais.fk_tbl_aulas_id_aula = tbl_aulas.id_aula
    """

    cursor.execute(sql)
    materiais = cursor.fetchall()

    print("\n===== MATERIAIS =====")
    for material in materiais:
        print(f"ID: {material[0]}")
        print(f"Material: {material[1]}")
        print(f"Tipo: {material[2]}")
        print(f"Tamanho: {material[3]}")
        print(f"Aula: {material[4]}")
        print("-" * 40)

    cursor.close()
    conexao.close()


def editar_material():

    listar_materiais()

    id_material = input("Digite o ID do material: ")
    nome = input("Novo nome do material: ")
    tipo = input("Novo tipo do material: ")
    tamanho = input("Novo tamanho do arquivo: ")

    listar_aulas()
    aula_id = int(input("Novo ID da aula: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_materiais
    SET nome_material = %s,
        tipo_material = %s,
        tam_arqu_material = %s,
        fk_tbl_aulas_id_aula = %s
    WHERE id_material = %s
    """

    cursor.execute(sql, (nome, tipo, tamanho, aula_id, id_material))
    conexao.commit()

    print("Material atualizado com sucesso!")

    cursor.close()
    conexao.close()


def excluir_material():

    listar_materiais()

    id_material = input("Digite o ID do material: ")
    confirmar = input("Tem certeza que deseja excluir este material? (S/N): ").upper()

    if confirmar != "S":
        print("Exclusão cancelada.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_materiais WHERE id_material = %s"

    try:
        cursor.execute(sql, (id_material,))
        conexao.commit()
        print("Material excluído com sucesso!")
    except IntegrityError:
        print("Não foi possível excluir este material, pois existem dados vinculados a ele.")
    finally:
        cursor.close()
        conexao.close()


def trilha_do_aluno():

    conexao = conectar()
    cursor = conexao.cursor()

    print("\n===== CURSOS DISPONÍVEIS =====")

    cursor.execute("""
    SELECT id_curso, titulo_curso
    FROM tbl_cursos
    """)

    cursos = cursor.fetchall()

    for curso in cursos:
        print(f"[{curso[0]}] {curso[1]}")

    id_curso = input("\nDigite o ID do curso: ")

    print("\n===== MÓDULOS =====")

    cursor.execute("""
    SELECT id_modulo, titulo_modulo
    FROM tbl_modulos
    WHERE fk_tbl_cursos_id_curso = %s
    """, (id_curso,))

    modulos = cursor.fetchall()

    for modulo in modulos:
        print(f"[{modulo[0]}] {modulo[1]}")

    id_modulo = input("\nDigite o ID do módulo: ")

    print("\n===== AULAS =====")

    cursor.execute("""
    SELECT titulo_aula, url_arqui_aula
    FROM tbl_aulas
    WHERE fk_tbl_modulos_id_modulo = %s
    """, (id_modulo,))

    aulas = cursor.fetchall()

    for aula in aulas:
        print(f"▶ {aula[0]}")
        print(f"Link: {aula[1]}")
        print("-" * 40)

    cursor.close()
    conexao.close()



def menu_aluno(nome_usuario):
   
    while True:
        print("\n==============================")
        print(f" ÁREA DO ALUNO - {nome_usuario}")
        print("==============================")
        print("1 - Listar cursos disponíveis")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            trilha_do_aluno()
        elif opcao == "0":
            print("Saindo da área do aluno...")
            break

        else:
            print("Opção inválida!")


def menu_usuarios():

    while True:

        print("\n==============================")
        print("     GERENCIAR USUÁRIOS")
        print("==============================")
        print("1 - Adicionar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Deletar usuário")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            atualizar_usuario()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_categorias():

    while True:

        print("\n==============================")
        print("    GERENCIAR CATEGORIAS")
        print("==============================")

        print("1 - Adicionar categoria")
        print("2 - Listar categorias")
        print("3 - Editar categoria")
        print("4 - Excluir categoria")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_categoria()
        elif opcao == "2":
            listar_categorias()
        elif opcao == "3":
            editar_categoria()
        elif opcao == "4":
            excluir_categoria()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_cursos():

    while True:

        print("\n==============================")
        print("      GERENCIAR CURSOS")
        print("==============================")
        print("1 - Adicionar curso")
        print("2 - Listar cursos")
        print("3 - Editar curso")
        print("4 - Excluir curso")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_curso()
        elif opcao == "2":
            listar_cursos()
        elif opcao == "3":
            editar_curso()
        elif opcao == "4":
            excluir_curso()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_modulos():

    while True:

        print("\n==============================")
        print("     GERENCIAR MÓDULOS")
        print("==============================")

        print("1 - Adicionar módulo")
        print("2 - Listar módulos")
        print("3 - Editar módulo")
        print("4 - Excluir módulo")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_modulo()
        elif opcao == "2":
            listar_modulos()
        elif opcao == "3":
            editar_modulo()
        elif opcao == "4":
            excluir_modulo()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_aulas():

    while True:

        print("\n==============================")
        print("      GERENCIAR AULAS")
        print("==============================")

        print("1 - Adicionar aula")
        print("2 - Listar aulas")
        print("3 - Editar aula")
        print("4 - Excluir aula")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_aula()
        elif opcao == "2":
            listar_aulas()
        elif opcao == "3":
            editar_aula()
        elif opcao == "4":
            excluir_aula()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_materiais():

    while True:

        print("\n==============================")
        print("    GERENCIAR MATERIAIS")
        print("==============================")

        print("1 - Adicionar material")
        print("2 - Listar materiais")
        print("3 - Editar material")
        print("4 - Excluir material")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_material()
        elif opcao == "2":
            listar_materiais()
        elif opcao == "3":
            editar_material()
        elif opcao == "4":
            excluir_material()
        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_admin():

    while True:

        print("\n==============================")
        print("     MENU ADMINISTRATIVO")
        print("==============================")
        
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar categorias")
        print("3 - Gerenciar cursos")
        print("4 - Gerenciar módulos")
        print("5 - Gerenciar aulas")
        print("6 - Gerenciar materiais")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_categorias()
        elif opcao == "3":
            menu_cursos()
        elif opcao == "4":
            menu_modulos()
        elif opcao == "5":
            menu_aulas()
        elif opcao == "6":
            menu_materiais()
        elif opcao == "0":
            print("Saindo do menu admin...")
            break

        else:
            print("Opção inválida!")


def tela_inicial():
    criar_tabelas()

    while True:
        print("\n==============================")
        print("          CORE STUDY")
        print("==============================")
        print("1 - Cadastre-se")
        print("2 - Fazer login")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            adicionar_usuario()
        elif opcao == "2":
            tipo_usuario, nome_usuario, id_usuario = logar_sistema()

            if tipo_usuario == "ADMIN":
                print(f"\nBem vindo, {nome_usuario}!")
                menu_admin()
            elif tipo_usuario == "ALUNO":
                print(f"\nBem-vindo, {nome_usuario}!")
                menu_aluno(nome_usuario)

            else:
                print("Acesso negado!")
        
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida!")
     

tela_inicial()



































