# Core Study - Critérios do Projeto

## Regras de negócio

- Todo curso deve estar vinculado a uma categoria existente.
- Todo curso deve ter carga horária maior que zero.
- Todo módulo deve estar vinculado a um curso existente.
- Toda aula deve estar vinculada a um módulo existente.
- Todo material deve estar vinculado a uma aula existente.
- Um email não pode ser cadastrado para mais de um usuário.
- Uma categoria não pode ser excluída enquanto possuir cursos vinculados.
- Um curso não pode ser excluído enquanto possuir módulos vinculados.
- Um módulo não pode ser excluído enquanto possuir aulas vinculadas.
- Uma aula não pode ser excluída enquanto possuir materiais vinculados.

## Modelo relacional

Entidades principais:

- `tbl_categoria`: armazena as categorias dos cursos.
- `tbl_cursos`: armazena cursos e pertence a uma categoria.
- `tbl_modulos`: armazena módulos e pertence a um curso.
- `tbl_aulas`: armazena aulas e pertence a um módulo.
- `tbl_materiais`: armazena materiais e pertence a uma aula.
- `tbl_usuarios`: armazena usuários/alunos.
- `usu_cur`: tabela associativa entre usuários e cursos.

Relacionamentos:

- `tbl_categoria` 1:N `tbl_cursos`
- `tbl_cursos` 1:N `tbl_modulos`
- `tbl_modulos` 1:N `tbl_aulas`
- `tbl_aulas` 1:N `tbl_materiais`
- `tbl_usuarios` N:N `tbl_cursos` por meio de `usu_cur`

## CRUD implementado

- Usuários: cadastrar, listar, editar e excluir.
- Categorias: cadastrar, listar, editar e excluir.
- Cursos: cadastrar, listar, editar e excluir.
- Módulos: cadastrar, listar, editar e excluir.
- Aulas: cadastrar, listar, editar e excluir.
- Materiais: cadastrar, listar, editar e excluir.

## Lógica computacional aplicada

- Condicionais para controle de acesso de aluno e administrador.
- Condicionais para validação de campos obrigatórios.
- Condicionais para impedir exclusões inválidas.
- Conversão e validação numérica da carga horária.
- Loops nos templates para listar cursos, módulos, aulas, materiais e usuários.
- Consultas SQL com `JOIN` para exibir informações relacionadas.
- Validações com quantificador existencial: antes de cadastrar um item filho, o sistema verifica se o item pai existe.

## Backlog SCRUM

- Como administrador, quero gerenciar categorias para organizar os cursos.
- Como administrador, quero gerenciar cursos para disponibilizar conteúdos aos alunos.
- Como administrador, quero gerenciar módulos para dividir os cursos em partes.
- Como administrador, quero gerenciar aulas para estruturar o conteúdo dos módulos.
- Como administrador, quero gerenciar materiais para apoiar os estudos.
- Como administrador, quero gerenciar usuários para controlar os alunos cadastrados.
- Como aluno, quero acessar minha trilha de estudos para visualizar cursos disponíveis.
- Como aluno, quero acessar aulas e materiais para estudar.
- Como sistema, quero validar dados antes de gravar no banco para evitar inconsistências.

## Planejamento de sprints

Sprint 1:
- Criar banco de dados.
- Criar tabelas principais.
- Configurar conexão MySQL.
- Implementar login e sessões.

Sprint 2:
- Implementar CRUD de usuários, categorias e cursos.
- Criar telas administrativas iniciais.

Sprint 3:
- Implementar CRUD de módulos, aulas e materiais.
- Criar área do aluno e navegação pela trilha.

Sprint 4:
- Padronizar layout.
- Tratar erros de exclusão.
- Adicionar validações de regras de negócio.
- Preparar apresentação final.

## Roteiro da apresentação

1. Explicar o objetivo do Core Study.
2. Mostrar a arquitetura: Flask, MySQL, HTML e CSS.
3. Apresentar o DER e os relacionamentos.
4. Demonstrar o login de administrador.
5. Demonstrar os CRUDs administrativos.
6. Demonstrar a área do aluno.
7. Explicar as regras de negócio e validações.
8. Mostrar o quadro SCRUM, backlog e sprints.
9. Encerrar com melhorias futuras.
