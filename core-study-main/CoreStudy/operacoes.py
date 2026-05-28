import getpass
from conexao import conectar

# --- USUÁRIOS E PERFIL ---
def adicionar_usuario():
    print("\n========================================")
    print("             NOVO CADASTRO              ")
    print("========================================")
    nome_completo = input("Nome Completo: ")
    
    # Validação de E-mail
    while True:
        email = input("E-mail: ")
        if "@" in email and "." in email:
            break
        else:
            print("\nFormato de e-mail inválido. Certifique-se de colocar '@' e o domínio (ex: .com).\n")
            
    telefone = input("Telefone: ")
    
    # Validação e conversão da Data de Nascimento (Formato BR para SQL)
    while True:
        data_brasil = input("Data de Nascimento (DD/MM/AAAA): ")
        try:
            partes_da_data = data_brasil.split('/')
            if len(partes_da_data) == 3:
                dia = partes_da_data[0]
                mes = partes_da_data[1]
                ano = partes_da_data[2]
                nascimento_formatado = f"{ano}-{mes}-{dia}"
                break
            else:
                print("\nFormato incorreto. Use as barras (/) para separar o dia, mês e ano.\n")
        except ValueError:
            print("\nFormato inválido. Digite exatamente como no exemplo: 15/04/2005.\n")
            
    # Confirmação de Senha
    while True:
        senha = getpass.getpass("Senha: ")
        confirmacao_senha = getpass.getpass("Confirme sua senha: ")
        if senha == confirmacao_senha:
            break
        else:
            print("\nAs senhas não coincidem. Tente novamente.\n")
    
    aceite_dos_termos = input("Aceita os termos de uso do Core Study? (S/N): ").upper()
    if aceite_dos_termos != 'S': 
        print("\nCadastro cancelado: É necessário aceitar os termos.\n")
        return

    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "INSERT INTO tbl_usuarios (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(comando_sql, (nome_completo, email, telefone, nascimento_formatado, senha))
            conexao.commit()
            print("\nUsuário cadastrado com sucesso!")
        except Exception as erro:
            print(f"\nFalha ao cadastrar no banco de dados: {erro}\n")
        finally:
            cursor.close()
            conexao.close()

def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tbl_usuarios")
    for usuario in cursor.fetchall(): 
        print(f"ID: {usuario[0]} | Nome: {usuario[1]} | E-mail: {usuario[2]}")
    cursor.close()
    conexao.close()

def visualizar_perfil(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    print("\n========================================")
    print("             SEUS DADOS                 ")
    print("========================================")
    print(f"Nome: {usuario['nome_usuario']}")
    print(f"E-mail: {usuario['email_usuario']}")
    print(f"Telefone: {usuario['telefone_usuario']}")
    print(f"Nascimento: {usuario['dt_nasc_usuario']}")
    print("========================================")
    cursor.close()
    conexao.close()

def editar_perfil(id_usuario):
    print("\n========================================")
    print("1 - Editar Nome Completo")
    print("2 - Editar Telefone")
    print("3 - Editar Senha")
    print("----------------------------------------")
    print("0 - Voltar")
    print("========================================")
    opcao = input("Escolha o que deseja editar: ")
    
    if opcao == "0":
        return
        
    campo_banco = {"1": "nome_usuario", "2": "telefone_usuario", "3": "senha_usuario"}.get(opcao)
    
    if not campo_banco:
        print("\nOpção inválida.\n")
        return
        
    novo_valor = getpass.getpass("Novo valor: ") if opcao == "3" else input("Novo valor: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(f"UPDATE tbl_usuarios SET {campo_banco} = %s WHERE id_usuario = %s", (novo_valor, id_usuario))
    conexao.commit()
    print("\nPerfil atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_conta(id_usuario):
    print("\nAtenção: Esta ação é irreversível.")
    if input("Tem certeza que deseja excluir sua conta? (S/N): ").upper() == 'S':
        senha = getpass.getpass("Confirme sua senha para excluir: ")
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_usuarios WHERE id_usuario = %s AND senha_usuario = %s", (id_usuario, senha))
        
        if cursor.rowcount > 0:
            conexao.commit()
            print("\nConta excluída com sucesso.")
            sucesso = True
        else:
            print("\nSenha incorreta. Exclusão cancelada.\n")
            sucesso = False
            
        cursor.close()
        conexao.close()
        return sucesso
    return False

# --- CATEGORIAS ---
def adicionar_categoria():
    nome_categoria = input("Nome da Categoria: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tbl_categoria (nome_categoria) VALUES (%s)", (nome_categoria,))
    conexao.commit()
    print("\nCategoria cadastrada!")
    cursor.close()
    conexao.close()

def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tbl_categoria")
    for categoria in cursor.fetchall(): 
        print(f"ID: {categoria[0]} | Nome: {categoria[1]}")
    cursor.close()
    conexao.close()

def editar_categoria():
    listar_categorias()
    id_categoria = input("ID da Categoria: ")
    novo_nome = input("Novo Nome da Categoria: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE tbl_categoria SET nome_categoria = %s WHERE id_categoria = %s", (novo_nome, id_categoria))
    conexao.commit()
    print("\nCategoria atualizada!")
    cursor.close()
    conexao.close()

def excluir_categoria():
    listar_categorias()
    id_categoria = input("ID da Categoria: ")
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM tbl_categoria WHERE id_categoria = %s", (id_categoria,))
        conexao.commit()
        print("\nCategoria excluída com sucesso!")
    except:
        print("\nNão é possível excluir uma categoria que possui cursos vinculados.\n")
    finally:
        cursor.close()
        conexao.close()

# --- CURSOS ---
def adicionar_curso():
    titulo = input("Título do Curso: ")
    descricao = input("Descrição do Curso: ")
    carga_horaria = input("Carga Horária: ")
    id_categoria = input("ID da Categoria: ")
    conexao = conectar()
    cursor = conexao.cursor()
    comando_sql = "INSERT INTO tbl_cursos (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria) VALUES (%s, %s, %s, %s)"
    cursor.execute(comando_sql, (titulo, descricao, carga_horaria, id_categoria))
    conexao.commit()
    print("\nCurso cadastrado!")
    cursor.close()
    conexao.close()

def listar_cursos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_curso, titulo_curso, descricao_curso, carga_hora_curso FROM tbl_cursos")
    lista_cursos = cursor.fetchall()
    
    if not lista_cursos:
        print("\nNenhum curso cadastrado.\n")
        cursor.close()
        conexao.close()
        return

    print("\n========================================")
    print("       VISÃO GERAL DO ADMINISTRADOR     ")
    print("========================================")
    for curso in lista_cursos:
        print(f"\n[ID CURSO: {curso[0]}] {curso[1]} ({curso[3]}h)")
        print(f"Descrição: {curso[2]}")
        
        cursor.execute("SELECT id_modulo, titulo_modulo FROM tbl_modulos WHERE fk_tbl_cursos_id_curso = %s", (curso[0],))
        modulos = cursor.fetchall()
        if not modulos:
            print("  └-- [Nenhum módulo cadastrado]")
            
        for modulo in modulos:
            print(f"  └-- [ID MÓDULO: {modulo[0]}] {modulo[1]}")
            cursor.execute("SELECT id_aula, titulo_aula, url_arqui_aula FROM tbl_aulas WHERE fk_tbl_modulos_id_modulo = %s", (modulo[0],))
            aulas = cursor.fetchall()
            if not aulas:
                print("        └-- [Nenhuma aula cadastrada]")
                
            for aula in aulas:
                print(f"        ▶ [ID AULA: {aula[0]}] {aula[1]} | {aula[2]}")
                cursor.execute("SELECT id_material, nome_material, tipo_material FROM tbl_materiais WHERE fk_tbl_aulas_id_aula = %s", (aula[0],))
                materiais = cursor.fetchall()
                for material in materiais:
                    print(f"            └-- [ID MATERIAL: {material[0]}] {material[1]} ({material[2]})")
        print("----------------------------------------")
        
    cursor.close()
    conexao.close()

def buscar_curso():
    print("\n========================================")
    print("             BUSCAR CURSO               ")
    print("========================================")
    print("1 - Buscar pelo Título do Curso")
    print("2 - Buscar pela Categoria")
    opcao_busca = input("Como deseja pesquisar? ")

    conexao = conectar()
    if not conexao:
        return

    cursor = conexao.cursor()

    if opcao_busca == "1":
        termo_pesquisa = input("Digite parte do título do curso: ")
        comando_sql = "SELECT id_curso, titulo_curso, descricao_curso FROM tbl_cursos WHERE titulo_curso LIKE %s"
        cursor.execute(comando_sql, (f"%{termo_pesquisa}%",))
        resultados = cursor.fetchall()
        
        print("\n--- Resultados Encontrados ---")
        if resultados:
            for linha in resultados:
                print(f"ID: {linha[0]} | Curso: {linha[1]} | Descrição: {linha[2]}")
        else:
            print("\nNenhum curso encontrado com esse título.\n")

    elif opcao_busca == "2":
        termo_pesquisa = input("Digite o nome da categoria: ")
        comando_sql = """
            SELECT cursos.id_curso, cursos.titulo_curso, categoria.nome_categoria 
            FROM tbl_cursos AS cursos
            INNER JOIN tbl_categoria AS categoria 
            ON cursos.fk_tbl_categoria_id_categoria = categoria.id_categoria
            WHERE categoria.nome_categoria LIKE %s
        """
        cursor.execute(comando_sql, (f"%{termo_pesquisa}%",))
        resultados = cursor.fetchall()
        
        print("\n--- Resultados Encontrados ---")
        if resultados:
            for linha in resultados:
                print(f"ID: {linha[0]} | Curso: {linha[1]} | Categoria: {linha[2]}")
        else:
            print("\nNenhum curso encontrado para essa categoria.\n")
    else:
        print("\nOpção de busca inválida.\n")

    cursor.close()
    conexao.close()

def editar_curso():
    listar_cursos()
    id_curso = input("ID do Curso que deseja editar: ")
    novo_titulo = input("Novo Título: ")
    nova_descricao = input("Nova Descrição: ")
    nova_carga = input("Nova Carga Horária: ")
    id_categoria = input("Novo ID da Categoria: ")
    conexao = conectar()
    cursor = conexao.cursor()
    comando_sql = "UPDATE tbl_cursos SET titulo_curso=%s, descricao_curso=%s, carga_hora_curso=%s, fk_tbl_categoria_id_categoria=%s WHERE id_curso=%s"
    cursor.execute(comando_sql, (novo_titulo, nova_descricao, nova_carga, id_categoria, id_curso))
    conexao.commit()
    print("\nCurso atualizado!")
    cursor.close()
    conexao.close()

def excluir_curso():
    listar_cursos()
    id_curso = input("ID do Curso: ")
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM tbl_cursos WHERE id_curso = %s", (id_curso,))
        conexao.commit()
        print("\nCurso excluído com sucesso!")
    except:
        print("\nNão é possível excluir um curso que possui módulos vinculados.\n")
    finally:
        cursor.close()
        conexao.close()

# --- MÓDULOS ---
def adicionar_modulo():
    titulo_modulo = input("Título do Módulo: ")
    id_curso = input("ID do Curso: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tbl_modulos (titulo_modulo, fk_tbl_cursos_id_curso) VALUES (%s, %s)", (titulo_modulo, id_curso))
    conexao.commit()
    print("\nMódulo cadastrado!")
    cursor.close()
    conexao.close()

def listar_modulos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tbl_modulos")
    for modulo in cursor.fetchall(): 
        print(f"ID: {modulo[0]} | Título: {modulo[1]}")
    cursor.close()
    conexao.close()

def editar_modulo():
    listar_modulos()
    id_modulo = input("ID do Módulo: ")
    novo_titulo = input("Novo Título: ")
    id_curso = input("Novo ID do Curso: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE tbl_modulos SET titulo_modulo=%s, fk_tbl_cursos_id_curso=%s WHERE id_modulo=%s", (novo_titulo, id_curso, id_modulo))
    conexao.commit()
    print("\nMódulo atualizado!")
    cursor.close()
    conexao.close()

def excluir_modulo():
    listar_modulos()
    id_modulo = input("ID do Módulo: ")
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM tbl_modulos WHERE id_modulo = %s", (id_modulo,))
        conexao.commit()
        print("\nMódulo excluído com sucesso!")
    except:
        print("\nNão é possível excluir um módulo que possui aulas vinculadas.\n")
    finally:
        cursor.close()
        conexao.close()

# --- AULAS ---
def adicionar_aula():
    titulo_aula = input("Título da Aula: ")
    url_aula = input("URL da Aula: ")
    id_modulo = input("ID do Módulo: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tbl_aulas (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo) VALUES (%s, %s, %s)", (titulo_aula, url_aula, id_modulo))
    conexao.commit()
    print("\nAula cadastrada!")
    cursor.close()
    conexao.close()

def listar_aulas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tbl_aulas")
    for aula in cursor.fetchall(): 
        print(f"ID: {aula[0]} | Título: {aula[1]}")
    cursor.close()
    conexao.close()

def editar_aula():
    listar_aulas()
    id_aula = input("ID da Aula: ")
    novo_titulo = input("Novo Título: ")
    nova_url = input("Nova URL: ")
    id_modulo = input("Novo ID do Módulo: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE tbl_aulas SET titulo_aula=%s, url_arqui_aula=%s, fk_tbl_modulos_id_modulo=%s WHERE id_aula=%s", (novo_titulo, nova_url, id_modulo, id_aula))
    conexao.commit()
    print("\nAula atualizada!")
    cursor.close()
    conexao.close()

def excluir_aula():
    listar_aulas()
    id_aula = input("ID da Aula: ")
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM tbl_aulas WHERE id_aula = %s", (id_aula,))
        conexao.commit()
        print("\nAula excluída com sucesso!")
    except:
        print("\nNão é possível excluir uma aula que possui materiais vinculados.\n")
    finally:
        cursor.close()
        conexao.close()

# --- MATERIAIS ---
def adicionar_material():
    nome_material = input("Nome do Material: ")
    tipo_material = input("Tipo do Material: ")
    tamanho = input("Tamanho: ")
    id_aula = input("ID da Aula: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tbl_materiais (nome_material, tipo_material, tam_arqu_material, fk_tbl_aulas_id_aula) VALUES (%s, %s, %s, %s)", (nome_material, tipo_material, tamanho, id_aula))
    conexao.commit()
    print("\nMaterial cadastrado!")
    cursor.close()
    conexao.close()

def listar_materiais():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tbl_materiais")
    for material in cursor.fetchall(): 
        print(f"ID: {material[0]} | Nome: {material[1]}")
    cursor.close()
    conexao.close()

def editar_material():
    listar_materiais()
    id_material = input("ID do Material: ")
    novo_nome = input("Novo Nome: ")
    novo_tipo = input("Novo Tipo: ")
    novo_tamanho = input("Novo Tamanho: ")
    id_aula = input("Novo ID da Aula: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE tbl_materiais SET nome_material=%s, tipo_material=%s, tam_arqu_material=%s, fk_tbl_aulas_id_aula=%s WHERE id_material=%s", (novo_nome, novo_tipo, novo_tamanho, id_aula, id_material))
    conexao.commit()
    print("\nMaterial atualizado!")
    cursor.close()
    conexao.close()

def excluir_material():
    listar_materiais()
    id_material = input("ID do Material: ")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tbl_materiais WHERE id_material = %s", (id_material,))
    conexao.commit()
    print("\nMaterial excluído com sucesso!")
    cursor.close()
    conexao.close()

# --- FLUXO DO ALUNO ---
def trilha_do_aluno():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos")
    print("\n========================================")
    print("          CATÁLOGO DE CURSOS            ")
    print("========================================")
    for curso in cursor.fetchall(): 
        print(f"ID: [{curso[0]}] - {curso[1]}")
    id_curso = input("\nDigite o ID do Curso para ver o conteúdo: ")
    
    cursor.execute("SELECT titulo_curso, descricao_curso FROM tbl_cursos WHERE id_curso = %s", (id_curso,))
    dados_curso = cursor.fetchone()
    if not dados_curso: 
        print("\nCurso não encontrado.\n")
        return
        
    print("\n========================================")
    print(f"CURSO: {dados_curso[0]}")
    print(f"DESCRIÇÃO: {dados_curso[1]}")
    print("========================================")
    
    cursor.execute("SELECT id_modulo, titulo_modulo FROM tbl_modulos WHERE fk_tbl_cursos_id_curso = %s", (id_curso,))
    for modulo in cursor.fetchall():
        print(f"\n[ MÓDULO: {modulo[1]} ]")
        cursor.execute("SELECT id_aula, titulo_aula, url_arqui_aula FROM tbl_aulas WHERE fk_tbl_modulos_id_modulo = %s", (modulo[0],))
        for aula in cursor.fetchall():
            print(f"  ▶ Aula: {aula[1]} | Link: {aula[2]}")
            cursor.execute("SELECT nome_material, tipo_material FROM tbl_materiais WHERE fk_tbl_aulas_id_aula = %s", (aula[0],))
            for material in cursor.fetchall(): 
                print(f"    └-- Material Anexo: {material[0]} ({material[1]})")
    
    print("\n========================================")
    cursor.close()
    conexao.close()