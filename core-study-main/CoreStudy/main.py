from conexao import criar_tabelas
from login import logar_sistema
from operacoes import *

def submenu_usuarios():
    while True:
        print("\n========================================")
        print("          GERENCIAR USUÁRIOS            ")
        print("========================================")
        print("1 - Listar Usuários")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": listar_usuarios()
        elif op == "0": break
        else: print("Opção inválida.")

def submenu_categorias():
    while True:
        print("\n========================================")
        print("         GERENCIAR CATEGORIAS           ")
        print("========================================")
        print("1 - Adicionar Categoria")
        print("2 - Listar Categorias")
        print("3 - Editar Categoria")
        print("4 - Excluir Categoria")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": adicionar_categoria()
        elif op == "2": listar_categorias()
        elif op == "3": editar_categoria()
        elif op == "4": excluir_categoria()
        elif op == "0": break
        else: print("Opção inválida.")

def submenu_cursos():
    while True:
        print("\n========================================")
        print("           GERENCIAR CURSOS             ")
        print("========================================")
        print("1 - Adicionar Curso")
        print("2 - Listar Cursos (Visão Geral)")
        print("3 - Editar Curso")
        print("4 - Excluir Curso")
        print("5 - Buscar Curso")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": adicionar_curso()
        elif op == "2": listar_cursos()
        elif op == "3": editar_curso()
        elif op == "4": excluir_curso()
        elif op == "5": buscar_curso()
        elif op == "0": break
        else: print("Opção inválida.")

def submenu_modulos():
    while True:
        print("\n========================================")
        print("          GERENCIAR MÓDULOS             ")
        print("========================================")
        print("1 - Adicionar Módulo")
        print("2 - Listar Módulos")
        print("3 - Editar Módulo")
        print("4 - Excluir Módulo")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": adicionar_modulo()
        elif op == "2": listar_modulos()
        elif op == "3": editar_modulo()
        elif op == "4": excluir_modulo()
        elif op == "0": break
        else: print("Opção inválida.")

def submenu_aulas():
    while True:
        print("\n========================================")
        print("            GERENCIAR AULAS             ")
        print("========================================")
        print("1 - Adicionar Aula")
        print("2 - Listar Aulas")
        print("3 - Editar Aula")
        print("4 - Excluir Aula")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": adicionar_aula()
        elif op == "2": listar_aulas()
        elif op == "3": editar_aula()
        elif op == "4": excluir_aula()
        elif op == "0": break
        else: print("Opção inválida.")

def submenu_materiais():
    while True:
        print("\n========================================")
        print("          GERENCIAR MATERIAIS           ")
        print("========================================")
        print("1 - Adicionar Material")
        print("2 - Listar Materiais")
        print("3 - Editar Material")
        print("4 - Excluir Material")
        print("----------------------------------------")
        print("0 - Voltar")
        print("========================================")
        op = input("Escolha uma opção: ")
        if op == "1": adicionar_material()
        elif op == "2": listar_materiais()
        elif op == "3": editar_material()
        elif op == "4": excluir_material()
        elif op == "0": break
        else: print("Opção inválida.")

def menu_admin():
    while True:
        print("\n========================================")
        print("         PAINEL ADMINISTRATIVO          ")
        print("========================================")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Categorias")
        print("3 - Gerenciar Cursos")
        print("4 - Gerenciar Módulos")
        print("5 - Gerenciar Aulas")
        print("6 - Gerenciar Materiais")
        print("----------------------------------------")
        print("0 - Fazer Logout")
        print("========================================")
        op = input("Escolha uma opção: ")
        
        if op == "1": submenu_usuarios()
        elif op == "2": submenu_categorias()
        elif op == "3": submenu_cursos()
        elif op == "4": submenu_modulos()
        elif op == "5": submenu_aulas()
        elif op == "6": submenu_materiais()
        elif op == "0": break
        else: print("Opção inválida.")

def menu_aluno(id_u, nome):
    while True:
        print(f"\n========================================")
        print(f"       ÁREA DO ALUNO: {nome}            ")
        print("========================================")
        print("1 - Catálogo de Cursos")
        print("2 - Buscar Curso")
        print("3 - Gerenciar Perfil")
        print("----------------------------------------")
        print("0 - Fazer Logout")
        print("========================================")
        op = input("Escolha uma opção: ")
        
        if op == "1": 
            trilha_do_aluno()
        elif op == "2":
            buscar_curso()
        elif op == "3":
            while True:
                print("\n========================================")
                print("           GERENCIAR PERFIL             ")
                print("========================================")
                print("1 - Visualizar Dados")
                print("2 - Editar Dados")
                print("3 - Excluir Conta")
                print("----------------------------------------")
                print("0 - Voltar")
                print("========================================")
                sub = input("Escolha uma opção: ")
                if sub == "1": visualizar_perfil(id_u)
                elif sub == "2": editar_perfil(id_u)
                elif sub == "3": 
                    if excluir_conta(id_u): return
                elif sub == "0": break
                else: print("Opção inválida.")
        elif op == "0": break
        else: print("Opção inválida.")

def menu_principal():
    criar_tabelas()
    while True:
        print("\n========================================")
        print("           SISTEMA CORE STUDY           ")
        print("========================================")
        print("1 - Cadastrar Aluno")
        print("2 - Logar no Sistema")
        print("----------------------------------------")
        print("0 - Encerrar Aplicação")
        print("========================================")
        op = input("Escolha uma opção: ")
        
        if op == "1": 
            adicionar_usuario()
        elif op == "2":
            p, n, id_u = logar_sistema()
            if p == "ADMIN": 
                menu_admin()
            elif p == "ALUNO": 
                menu_aluno(id_u, n)
        elif op == "0": 
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()