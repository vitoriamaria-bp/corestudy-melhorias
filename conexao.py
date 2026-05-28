from flask import Flask, render_template, request, redirect, session
from mysql.connector import IntegrityError
from conexao import conectar

app = Flask(__name__)
app.secret_key = "corestudy_secret_key"
print(app.root_path)


@app.route("/")
def home():
    return render_template("index.html")


def verificar_admin():

    if "tipo_usuario" not in session:
        return False

    if session["tipo_usuario"] != "ADMIN":
        return False

    return True


def erro_validacao(mensagem, voltar):

    return render_template(
        "erro_exclusao.html",
        titulo="Erro de validação",
        mensagem=mensagem,
        voltar=voltar
    )


def campo_vazio(valor):

    return valor is None or valor.strip() == ""


def carga_hora_valida(carga_hora):

    try:
        return int(carga_hora) > 0
    except ValueError:
        return False


def registro_existe(cursor, tabela, coluna, valor):

    sql = f"""
    SELECT COUNT(*)
    FROM {tabela}
    WHERE {coluna} = %s
    """

    cursor.execute(sql, (valor,))
    return cursor.fetchone()[0] > 0


def email_em_uso(cursor, email, id_usuario=None):

    if id_usuario is None:
        sql = """
        SELECT COUNT(*)
        FROM tbl_usuarios
        WHERE email_usuario = %s
        """
        cursor.execute(sql, (email,))

    else:
        sql = """
        SELECT COUNT(*)
        FROM tbl_usuarios
        WHERE email_usuario = %s
        AND id_usuario <> %s
        """
        cursor.execute(sql, (email, id_usuario))

    return cursor.fetchone()[0] > 0


def categoria_em_uso(cursor, nome_categoria, id_categoria=None):

    if id_categoria is None:
        sql = """
        SELECT COUNT(*)
        FROM tbl_categoria
        WHERE nome_categoria = %s
        """
        cursor.execute(sql, (nome_categoria,))

    else:
        sql = """
        SELECT COUNT(*)
        FROM tbl_categoria
        WHERE nome_categoria = %s
        AND id_categoria <> %s
        """
        cursor.execute(sql, (nome_categoria, id_categoria))

    return cursor.fetchone()[0] > 0


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        if email == "admin" and senha == "admin":
            session["tipo_usuario"] = "ADMIN"
            session["nome_usuario"] = "Administrador"
            session["id_usuario"] = 0

            return redirect("/admin")

        conexao = conectar()
        cursor = conexao.cursor(buffered=True)

        sql = """
        SELECT id_usuario, nome_usuario
        FROM tbl_usuarios
        WHERE email_usuario = %s
        AND senha_usuario = %s
        """

        cursor.execute(sql, (email, senha))
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if usuario:
            session["tipo_usuario"] = "ALUNO"
            session["nome_usuario"] = usuario[1]
            session["id_usuario"] = usuario[0]

            return redirect("/aluno")

        else:
            return render_template(
                "login_erro.html",
                mensagem="Email ou senha inválidos."
            )

    return render_template("login.html")

@app.route("/admin")
def admin():

    if "tipo_usuario" not in session:
        return redirect("/login")

    if session["tipo_usuario"] != "ADMIN":
        return redirect("/aluno")

    return render_template(
        "admin.html",
        nome_usuario=session["nome_usuario"]
    )


@app.route("/aluno")
def aluno():

    if "tipo_usuario" not in session:
        return redirect("/login")

    if session["tipo_usuario"] != "ALUNO":
        return redirect("/admin")

    return render_template(
        "aluno.html",
        nome_usuario=session["nome_usuario"]
    )

@app.route("/trilha")
def trilha():

    if "tipo_usuario" not in session:
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_cursos.id_curso,
           tbl_cursos.titulo_curso,
           tbl_cursos.descricao_curso,
           tbl_cursos.carga_hora_curso,
           tbl_categoria.nome_categoria
    FROM tbl_cursos
    LEFT JOIN tbl_categoria
    ON tbl_cursos.fk_tbl_categoria_id_categoria = tbl_categoria.id_categoria
    ORDER BY tbl_categoria.nome_categoria ASC,
             tbl_cursos.titulo_curso ASC
    """

    cursor.execute(sql)
    cursos = cursor.fetchall()

    cursos_por_categoria = []

    for curso in cursos:
        nome_categoria = curso[4] or "Sem categoria"

        if (
            not cursos_por_categoria
            or cursos_por_categoria[-1]["nome_categoria"] != nome_categoria
        ):
            cursos_por_categoria.append({
                "nome_categoria": nome_categoria,
                "cursos": []
            })

        cursos_por_categoria[-1]["cursos"].append(curso)

    cursor.close()
    conexao.close()

    return render_template(
        "trilha.html",
        cursos_por_categoria=cursos_por_categoria,
        nome_usuario=session["nome_usuario"]
    )


@app.route("/trilha/curso/<int:id_curso>")
def visualizar_curso(id_curso):

    if "tipo_usuario" not in session:
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql_curso = """
    SELECT titulo_curso, descricao_curso
    FROM tbl_cursos
    WHERE id_curso = %s
    """

    cursor.execute(sql_curso, (id_curso,))
    curso = cursor.fetchone()

    sql_modulos = """
    SELECT id_modulo, titulo_modulo
    FROM tbl_modulos
    WHERE fk_tbl_cursos_id_curso = %s
    """

    cursor.execute(sql_modulos, (id_curso,))
    modulos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "curso_aluno.html",
        curso=curso,
        modulos=modulos,
        nome_usuario=session["nome_usuario"]
    )

@app.route("/trilha/modulo/<int:id_modulo>")
def visualizar_modulo(id_modulo):

    if "tipo_usuario" not in session:
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql_modulo = """
    SELECT titulo_modulo
    FROM tbl_modulos
    WHERE id_modulo = %s
    """

    cursor.execute(sql_modulo, (id_modulo,))
    modulo = cursor.fetchone()

    sql_aulas = """
    SELECT id_aula,
           titulo_aula,
           url_arqui_aula
    FROM tbl_aulas
    WHERE fk_tbl_modulos_id_modulo = %s
    """

    cursor.execute(sql_aulas, (id_modulo,))
    aulas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "modulo_aluno.html",
        modulo=modulo,
        aulas=aulas,
        nome_usuario=session["nome_usuario"]
    )

@app.route("/trilha/aula/<int:id_aula>")
def visualizar_aula(id_aula):

    if "tipo_usuario" not in session:
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql_aula = """
    SELECT titulo_aula,
           url_arqui_aula
    FROM tbl_aulas
    WHERE id_aula = %s
    """

    cursor.execute(sql_aula, (id_aula,))
    aula = cursor.fetchone()

    sql_materiais = """
    SELECT nome_material,
           tipo_material,
           tam_arqu_material
    FROM tbl_materiais
    WHERE fk_tbl_aulas_id_aula = %s
    """

    cursor.execute(sql_materiais, (id_aula,))
    materiais = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "aula_aluno.html",
        aula=aula,
        materiais=materiais,
        nome_usuario=session["nome_usuario"]
    )

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        data_nasc = request.form["data_nasc"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        if (
            campo_vazio(nome)
            or campo_vazio(email)
            or campo_vazio(telefone)
            or campo_vazio(data_nasc)
            or campo_vazio(senha)
        ):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha todos os campos para concluir o cadastro.",
                "/cadastro"
            )

        if email_em_uso(cursor, email):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Este email ja esta cadastrado. Use outro email para criar a conta.",
                "/cadastro"
            )

        sql = """
        INSERT INTO tbl_usuarios
        (
            nome_usuario,
            email_usuario,
            telefone_usuario,
            dt_nasc_usuario,
            senha_usuario
        )

        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            nome,
            email,
            telefone,
            data_nasc,
            senha
        )

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template("cadastro_sucesso.html")

    return render_template("cadastro.html")


@app.route("/admin/usuarios")
def usuarios():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_usuario,
           nome_usuario,
           email_usuario,
           telefone_usuario,
           dt_nasc_usuario,
           dt_cad_usuario
    FROM tbl_usuarios
    """

    cursor.execute(sql)
    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/admin/adicionar-usuario", methods=["GET", "POST"])
def adicionar_usuario_admin():

    if not verificar_admin():
        return redirect("/login")

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        data_nasc = request.form["data_nasc"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        if (
            campo_vazio(nome)
            or campo_vazio(email)
            or campo_vazio(telefone)
            or campo_vazio(data_nasc)
            or campo_vazio(senha)
        ):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha todos os campos para cadastrar o usuario.",
                "/admin/adicionar-usuario"
            )

        if email_em_uso(cursor, email):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Este email ja esta cadastrado para outro usuario.",
                "/admin/adicionar-usuario"
            )

        sql = """
        INSERT INTO tbl_usuarios
        (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nome, email, telefone, data_nasc, senha))
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect("/admin/usuarios")

    return render_template("adicionar_usuario.html")


@app.route("/admin/editar-usuario/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario_admin(id_usuario):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        data_nasc = request.form["data_nasc"]
        senha = request.form["senha"]

        if (
            campo_vazio(nome)
            or campo_vazio(email)
            or campo_vazio(telefone)
            or campo_vazio(data_nasc)
            or campo_vazio(senha)
        ):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha todos os campos para atualizar o usuario.",
                f"/admin/editar-usuario/{id_usuario}"
            )

        if email_em_uso(cursor, email, id_usuario):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Este email ja esta cadastrado para outro usuario.",
                f"/admin/editar-usuario/{id_usuario}"
            )

        sql = """
        UPDATE tbl_usuarios
        SET nome_usuario = %s,
            email_usuario = %s,
            telefone_usuario = %s,
            dt_nasc_usuario = %s,
            senha_usuario = %s
        WHERE id_usuario = %s
        """

        cursor.execute(sql, (nome, email, telefone, data_nasc, senha, id_usuario))
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect("/admin/usuarios")

    sql = """
    SELECT id_usuario,
           nome_usuario,
           email_usuario,
           telefone_usuario,
           dt_nasc_usuario,
           senha_usuario
    FROM tbl_usuarios
    WHERE id_usuario = %s
    """

    cursor.execute(sql, (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("editar_usuario.html", usuario=usuario)


@app.route("/admin/excluir-usuario/<int:id_usuario>", methods=["GET", "POST"])
def excluir_usuario_admin(id_usuario):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        sql = """
        DELETE FROM tbl_usuarios
        WHERE id_usuario = %s
        """

        cursor.execute(sql, (id_usuario,))
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect("/admin/usuarios")

    sql = """
    SELECT id_usuario, nome_usuario
    FROM tbl_usuarios
    WHERE id_usuario = %s
    """

    cursor.execute(sql, (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("confirmar_exclusao_usuario.html", usuario=usuario)


@app.route("/cursos")
def cursos():

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_curso,
       titulo_curso,
       descricao_curso,
       carga_hora_curso
    FROM tbl_cursos
    """

    cursor.execute(sql)

    cursos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("cursos.html", cursos=cursos, admin=False)

@app.route("/admin/cursos")
def cursos_admin():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT tbl_cursos.id_curso,
           tbl_cursos.titulo_curso,
           tbl_cursos.descricao_curso,
           tbl_cursos.carga_hora_curso,
           tbl_categoria.nome_categoria
    FROM tbl_cursos
    LEFT JOIN tbl_categoria
    ON tbl_cursos.fk_tbl_categoria_id_categoria = tbl_categoria.id_categoria
    """

    cursor.execute(sql)
    cursos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("cursos.html", cursos=cursos, admin=True)

@app.route("/admin/adicionar-curso", methods=["GET", "POST"])
def adicionar_curso():

    if not verificar_admin():
        return redirect("/login")

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        carga_hora = request.form["carga_hora"]
        categoria_id = request.form["categoria_id"]

        conexao = conectar()
        cursor = conexao.cursor()

        if campo_vazio(titulo) or campo_vazio(descricao):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha o titulo e a descricao do curso.",
                "/admin/adicionar-curso"
            )

        if not carga_hora_valida(carga_hora):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "A carga horaria do curso deve ser maior que zero.",
                "/admin/adicionar-curso"
            )

        if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione uma categoria valida para cadastrar o curso.",
                "/admin/adicionar-curso"
            )

        sql = """
        INSERT INTO tbl_cursos
        (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (titulo, descricao, carga_hora, categoria_id))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Curso cadastrado com sucesso.",
            voltar="/admin/cursos"
        )
    
    conexao = conectar()
    cursor = conexao.cursor()

    sql_categoria = """
    SELECT id_categoria, nome_categoria
    FROM tbl_categoria
    """

    cursor.execute(sql_categoria)

    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
    "adicionar_curso.html",
    categorias=categorias
    )

@app.route("/admin/editar-curso/<int:id_curso>", methods=["GET", "POST"])
def editar_curso(id_curso):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        carga_hora = request.form["carga_hora"]
        categoria_id = request.form["categoria_id"]

        if campo_vazio(titulo) or campo_vazio(descricao):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha o titulo e a descricao do curso.",
                f"/admin/editar-curso/{id_curso}"
            )

        if not carga_hora_valida(carga_hora):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "A carga horaria do curso deve ser maior que zero.",
                f"/admin/editar-curso/{id_curso}"
            )

        if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione uma categoria valida para atualizar o curso.",
                f"/admin/editar-curso/{id_curso}"
            )

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

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Curso atualizado com sucesso.",
            voltar="/admin/cursos"
        )

    sql = """
    SELECT id_curso,
           titulo_curso,
           descricao_curso,
           carga_hora_curso,
           fk_tbl_categoria_id_categoria
    FROM tbl_cursos
    WHERE id_curso = %s
    """

    cursor.execute(sql, (id_curso,))
    curso = cursor.fetchone()

    sql_categoria = """
    SELECT id_categoria, nome_categoria
    FROM tbl_categoria
    """

    cursor.execute(sql_categoria)
    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_curso.html",
        curso=curso,
        categorias=categorias
    )

@app.route("/admin/excluir-curso/<int:id_curso>", methods=["GET", "POST"])
def excluir_curso(id_curso):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        sql_delete = """
        DELETE FROM tbl_cursos
        WHERE id_curso = %s
        """

        try:
            cursor.execute(sql_delete, (id_curso,))
            conexao.commit()

        except IntegrityError:
            cursor.close()
            conexao.close()

            return render_template(
                "erro_exclusao.html",
                mensagem="Nao e possivel excluir este curso porque ele possui modulos cadastrados. Exclua os modulos primeiro.",
                voltar="/admin/cursos",
                acao_extra="/admin/modulos",
                texto_acao_extra="Ir para modulos"
                )

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Curso excluido com sucesso.",
            voltar="/admin/cursos"
        )

    sql = """
    SELECT *
    FROM tbl_cursos
    WHERE id_curso = %s
    """

    cursor.execute(sql, (id_curso,))
    curso = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "confirmar_exclusao.html",
        curso=curso
    )

@app.route("/admin/categorias")
def categorias():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_categoria, nome_categoria
    FROM tbl_categoria
    """

    cursor.execute(sql)
    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("categorias.html", categorias=categorias)

@app.route("/admin/adicionar-categoria", methods=["GET", "POST"])
def adicionar_categoria():

    if not verificar_admin():
        return redirect("/login")

    if request.method == "POST":

        nome_categoria = request.form["nome_categoria"]

        conexao = conectar()
        cursor = conexao.cursor()

        if campo_vazio(nome_categoria):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Informe o nome da categoria.",
                "/admin/adicionar-categoria"
            )

        if categoria_em_uso(cursor, nome_categoria):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Ja existe uma categoria cadastrada com esse nome.",
                "/admin/adicionar-categoria"
            )

        sql = """
        INSERT INTO tbl_categoria (nome_categoria)
        VALUES (%s)
        """

        cursor.execute(sql, (nome_categoria,))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Categoria cadastrada com sucesso.",
            voltar="/admin/categorias"
        )

    return render_template("adicionar_categoria.html")

@app.route("/admin/editar-categoria/<int:id_categoria>", methods=["GET", "POST"])
def editar_categoria(id_categoria):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome_categoria = request.form["nome_categoria"]

        if campo_vazio(nome_categoria):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Informe o nome da categoria.",
                f"/admin/editar-categoria/{id_categoria}"
            )

        if categoria_em_uso(cursor, nome_categoria, id_categoria):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Ja existe outra categoria cadastrada com esse nome.",
                f"/admin/editar-categoria/{id_categoria}"
            )

        sql = """
        UPDATE tbl_categoria
        SET nome_categoria = %s
        WHERE id_categoria = %s
        """

        cursor.execute(sql, (nome_categoria, id_categoria))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Categoria atualizada com sucesso.",
            voltar="/admin/categorias"
        )

    sql = """
    SELECT id_categoria, nome_categoria
    FROM tbl_categoria
    WHERE id_categoria = %s
    """

    cursor.execute(sql, (id_categoria,))
    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("editar_categoria.html", categoria=categoria)

@app.route("/admin/excluir-categoria/<int:id_categoria>", methods=["GET", "POST"])
def excluir_categoria(id_categoria):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        sql = """
        DELETE FROM tbl_categoria
        WHERE id_categoria = %s
        """

        try:
            cursor.execute(sql, (id_categoria,))
            conexao.commit()

        except IntegrityError:
            cursor.close()
            conexao.close()

            return render_template(
                "erro_exclusao.html",
                mensagem="Nao e possivel excluir esta categoria porque existem cursos vinculados a ela. Exclua ou edite esses cursos primeiro.",
                voltar="/admin/categorias",
                acao_extra="/admin/cursos",
                texto_acao_extra="Ir para cursos"
            )

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Categoria excluida com sucesso.",
            voltar="/admin/categorias"
        )

    sql = """
    SELECT id_categoria, nome_categoria
    FROM tbl_categoria
    WHERE id_categoria = %s
    """

    cursor.execute(sql, (id_categoria,))
    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "confirmar_exclusao_categoria.html",
        categoria=categoria
    )

@app.route("/admin/modulos")
def modulos():

    if not verificar_admin():
        return redirect("/login")

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

    cursor.close()
    conexao.close()

    return render_template(
        "modulos.html",
        modulos=modulos
    )


@app.route("/admin/adicionar-modulo", methods=["GET", "POST"])
def adicionar_modulo():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        curso_id = request.form["curso_id"]

        if campo_vazio(titulo):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Informe o titulo do modulo.",
                "/admin/adicionar-modulo"
            )

        if not registro_existe(cursor, "tbl_cursos", "id_curso", curso_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione um curso valido para cadastrar o modulo.",
                "/admin/adicionar-modulo"
            )

        sql = """
        INSERT INTO tbl_modulos
        (titulo_modulo, fk_tbl_cursos_id_curso)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (titulo, curso_id))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Modulo cadastrado com sucesso.",
            voltar="/admin/modulos"
        )

    sql_cursos = """
    SELECT id_curso, titulo_curso
    FROM tbl_cursos
    """

    cursor.execute(sql_cursos)

    cursos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "adicionar_modulo.html",
        cursos=cursos
    )


@app.route("/admin/editar-modulo/<int:id_modulo>", methods=["GET", "POST"])
def editar_modulo(id_modulo):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        curso_id = request.form["curso_id"]

        if campo_vazio(titulo):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Informe o titulo do modulo.",
                f"/admin/editar-modulo/{id_modulo}"
            )

        if not registro_existe(cursor, "tbl_cursos", "id_curso", curso_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione um curso valido para atualizar o modulo.",
                f"/admin/editar-modulo/{id_modulo}"
            )

        sql_update = """
        UPDATE tbl_modulos
        SET titulo_modulo = %s,
            fk_tbl_cursos_id_curso = %s
        WHERE id_modulo = %s
        """

        cursor.execute(sql_update, (titulo, curso_id, id_modulo))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Modulo atualizado com sucesso.",
            voltar="/admin/modulos"
        )

    sql_modulo = """
    SELECT id_modulo,
           titulo_modulo,
           fk_tbl_cursos_id_curso
    FROM tbl_modulos
    WHERE id_modulo = %s
    """

    cursor.execute(sql_modulo, (id_modulo,))
    modulo = cursor.fetchone()

    sql_cursos = """
    SELECT id_curso, titulo_curso
    FROM tbl_cursos
    """

    cursor.execute(sql_cursos)
    cursos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_modulo.html",
        modulo=modulo,
        cursos=cursos
    )


@app.route("/admin/excluir-modulo/<int:id_modulo>", methods=["GET", "POST"])
def excluir_modulo(id_modulo):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == 'POST':

        try:
            cursor.execute(
                "DELETE FROM tbl_modulos WHERE id_modulo = %s",
                (id_modulo,)
            )

            conexao.commit()

        except IntegrityError:
            cursor.close()
            conexao.close()

            return render_template(
                "erro_exclusao.html",
                mensagem="Nao e possivel excluir este modulo porque existem aulas vinculadas a ele. Exclua as aulas primeiro.",
                voltar="/admin/modulos",
                acao_extra="/admin/aulas",
                texto_acao_extra="Ir para aulas"
            )

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Modulo excluido com sucesso.",
            voltar="/admin/modulos"
        )

    sql = """
    SELECT *
    FROM tbl_modulos
    WHERE id_modulo = %s
    """

    cursor.execute(sql, (id_modulo,))
    modulo = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "confirmar_exclusao_modulo.html",
        modulo=modulo
    )

@app.route("/admin/aulas")
def aulas():

    if not verificar_admin():
        return redirect("/login")

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

    cursor.close()
    conexao.close()

    return render_template("aulas.html", aulas=aulas)


@app.route("/admin/adicionar-aula", methods=["GET", "POST"])
def adicionar_aula():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        url = request.form["url"]
        modulo_id = request.form["modulo_id"]

        if campo_vazio(titulo) or campo_vazio(url):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha o titulo e a URL da aula.",
                "/admin/adicionar-aula"
            )

        if not registro_existe(cursor, "tbl_modulos", "id_modulo", modulo_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione um modulo valido para cadastrar a aula.",
                "/admin/adicionar-aula"
            )

        sql = """
        INSERT INTO tbl_aulas
        (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (titulo, url, modulo_id))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Aula cadastrada com sucesso.",
            voltar="/admin/aulas"
        )

    sql_modulos = """
    SELECT tbl_modulos.id_modulo,
           tbl_modulos.titulo_modulo,
           tbl_cursos.titulo_curso
    FROM tbl_modulos
    INNER JOIN tbl_cursos
    ON tbl_modulos.fk_tbl_cursos_id_curso = tbl_cursos.id_curso
    """

    cursor.execute(sql_modulos)
    modulos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("adicionar_aula.html", modulos=modulos)


@app.route("/admin/editar-aula/<int:id_aula>", methods=["GET", "POST"])
def editar_aula(id_aula):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        url = request.form["url"]
        modulo_id = request.form["modulo_id"]

        if campo_vazio(titulo) or campo_vazio(url):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha o titulo e a URL da aula.",
                f"/admin/editar-aula/{id_aula}"
            )

        if not registro_existe(cursor, "tbl_modulos", "id_modulo", modulo_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione um modulo valido para atualizar a aula.",
                f"/admin/editar-aula/{id_aula}"
            )

        sql_update = """
        UPDATE tbl_aulas
        SET titulo_aula = %s,
            url_arqui_aula = %s,
            fk_tbl_modulos_id_modulo = %s
        WHERE id_aula = %s
        """

        cursor.execute(sql_update, (titulo, url, modulo_id, id_aula))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Aula atualizada com sucesso.",
            voltar="/admin/aulas"
        )

    sql_aula = """
    SELECT id_aula,
           titulo_aula,
           url_arqui_aula,
           fk_tbl_modulos_id_modulo
    FROM tbl_aulas
    WHERE id_aula = %s
    """

    cursor.execute(sql_aula, (id_aula,))
    aula = cursor.fetchone()

    sql_modulos = """
    SELECT tbl_modulos.id_modulo,
           tbl_modulos.titulo_modulo,
           tbl_cursos.titulo_curso
    FROM tbl_modulos
    INNER JOIN tbl_cursos
    ON tbl_modulos.fk_tbl_cursos_id_curso = tbl_cursos.id_curso
    """

    cursor.execute(sql_modulos)
    modulos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_aula.html",
        aula=aula,
        modulos=modulos
    )


@app.route("/admin/excluir-aula/<int:id_aula>", methods=["GET", "POST"])
def excluir_aula(id_aula):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        sql_delete = """
        DELETE FROM tbl_aulas
        WHERE id_aula = %s
        """

        try:
            cursor.execute(sql_delete, (id_aula,))
            conexao.commit()

        except IntegrityError:
            cursor.close()
            conexao.close()

            return render_template(
                "erro_exclusao.html",
                mensagem="Nao e possivel excluir esta aula porque existem materiais vinculados a ela. Exclua os materiais primeiro.",
                voltar="/admin/aulas",
                acao_extra="/admin/materiais",
                texto_acao_extra="Ir para materiais"
            )

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Aula excluida com sucesso.",
            voltar="/admin/aulas"
        )

    sql = """
    SELECT id_aula, titulo_aula
    FROM tbl_aulas
    WHERE id_aula = %s
    """

    cursor.execute(sql, (id_aula,))
    aula = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("confirmar_exclusao_aula.html", aula=aula)


@app.route("/admin/materiais")
def materiais():

    if not verificar_admin():
        return redirect("/login")

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

    cursor.close()
    conexao.close()

    return render_template(
        "materiais.html",
        materiais=materiais
    )


@app.route("/admin/adicionar-material", methods=["GET", "POST"])
def adicionar_material():

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        tipo = request.form["tipo"]
        tamanho = request.form["tamanho"]
        aula_id = request.form["aula_id"]

        if campo_vazio(nome) or campo_vazio(tipo) or campo_vazio(tamanho):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha nome, tipo e tamanho do material.",
                "/admin/adicionar-material"
            )

        if not registro_existe(cursor, "tbl_aulas", "id_aula", aula_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione uma aula valida para cadastrar o material.",
                "/admin/adicionar-material"
            )

        sql = """
        INSERT INTO tbl_materiais
        (
            nome_material,
            tipo_material,
            tam_arqu_material,
            fk_tbl_aulas_id_aula
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (nome, tipo, tamanho, aula_id))
        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Material cadastrado com sucesso.",
            voltar="/admin/materiais"
        )

    sql_aulas = """
    SELECT id_aula, titulo_aula
    FROM tbl_aulas
    """

    cursor.execute(sql_aulas)
    aulas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "adicionar_material.html",
        aulas=aulas
    )


@app.route("/admin/editar-material/<int:id_material>", methods=["GET", "POST"])
def editar_material(id_material):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        tipo = request.form["tipo"]
        tamanho = request.form["tamanho"]
        aula_id = request.form["aula_id"]

        if campo_vazio(nome) or campo_vazio(tipo) or campo_vazio(tamanho):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Preencha nome, tipo e tamanho do material.",
                f"/admin/editar-material/{id_material}"
            )

        if not registro_existe(cursor, "tbl_aulas", "id_aula", aula_id):
            cursor.close()
            conexao.close()
            return erro_validacao(
                "Selecione uma aula valida para atualizar o material.",
                f"/admin/editar-material/{id_material}"
            )

        sql_update = """
        UPDATE tbl_materiais
        SET nome_material = %s,
            tipo_material = %s,
            tam_arqu_material = %s,
            fk_tbl_aulas_id_aula = %s
        WHERE id_material = %s
        """

        cursor.execute(
            sql_update,
            (nome, tipo, tamanho, aula_id, id_material)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Material atualizado com sucesso.",
            voltar="/admin/materiais"
        )

    sql_material = """
    SELECT id_material,
           nome_material,
           tipo_material,
           tam_arqu_material,
           fk_tbl_aulas_id_aula
    FROM tbl_materiais
    WHERE id_material = %s
    """

    cursor.execute(sql_material, (id_material,))
    material = cursor.fetchone()

    sql_aulas = """
    SELECT id_aula, titulo_aula
    FROM tbl_aulas
    """

    cursor.execute(sql_aulas)
    aulas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_material.html",
        material=material,
        aulas=aulas
    )


@app.route("/admin/excluir-material/<int:id_material>", methods=["GET", "POST"])
def excluir_material(id_material):

    if not verificar_admin():
        return redirect("/login")

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        sql_delete = """
        DELETE FROM tbl_materiais
        WHERE id_material = %s
        """

        try:
            cursor.execute(sql_delete, (id_material,))
            conexao.commit()

        except IntegrityError:
            cursor.close()
            conexao.close()

            return render_template(
                "erro_exclusao.html",
                mensagem="Nao e possivel excluir este material porque existem registros vinculados a ele.",
                voltar="/admin/materiais"
            )

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            titulo="Sucesso!",
            mensagem="Material excluido com sucesso.",
            voltar="/admin/materiais"
        )

    sql = """
    SELECT id_material, nome_material
    FROM tbl_materiais
    WHERE id_material = %s
    """

    cursor.execute(sql, (id_material,))
    material = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "confirmar_exclusao_material.html",
        material=material
    )

if __name__ == "__main__":
    app.run(debug=True)
