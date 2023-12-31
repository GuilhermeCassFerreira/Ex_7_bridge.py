# API de Tarefas (Tasks API)

A API de Tarefas é uma aplicação simples que permite gerenciar tarefas (tasks) com autenticação de usuário. Esta API foi construída usando o framework Flask e se integra ao banco de dados PostgreSQL. Ela oferece funcionalidades para criar, listar, atualizar e excluir tarefas, além de fornecer autenticação de usuário baseada em JWT (JSON Web Tokens).

## Configuração e Instalação

Para executar a API de Tarefas em seu ambiente local, siga as etapas de configuração e instalação abaixo:

### 1. Configuração do Ambiente

Certifique-se de que você tenha os seguintes requisitos em seu ambiente:

- Python 3 instalado em seu sistema.
- PostgreSQL instalado e configurado, com um banco de dados chamado 'postgres', um usuário 'postgres' e senha 'AG123'. Você pode ajustar essas configurações no código, se necessário.
- Pip (gerenciador de pacotes Python) instalado em seu sistema.

### 2. Instalação das Dependências

Use o pip para instalar as dependências necessárias:

```
pip install Flask Flask-JWT-Extended peewee psycopg2-binary bcrypt
```

## Banco de Dados

A API utiliza um banco de dados PostgreSQL para armazenar informações de usuários e tarefas. O esquema do banco de dados inclui duas tabelas principais:

### Tabela 'users'

- `id` (Chave Primária): Identificador exclusivo de usuário.
- `username`: Nome de usuário único.
- `email`: Endereço de e-mail único.
- `password`: Senha do usuário (criptografada, não armazenada como texto claro).
- `admin`: Indica se o usuário possui privilégios de administrador.
- `auth_token`: Token de autenticação JWT (JSON Web Token) para autenticação do usuário.

### Tabela 'tasks'

- `id` (Chave Primária): Identificador exclusivo de tarefa.
- `title`: Título da tarefa.
- `completed`: Indica se a tarefa foi concluída (true/false).

As senhas dos usuários são armazenadas de forma criptografada usando a função `bcrypt` para garantir a segurança dos dados do usuário.

## Executando a API

Após configurar o ambiente e instalar as dependências, você pode iniciar a API. Siga estas etapas:

1. Certifique-se de estar na pasta onde o arquivo `ex_7_bridge.py` está localizado.

2. Execute o seguinte comando para iniciar a API:

```
python ex_7_bridge.py
```

A API estará acessível em `http://localhost:5000`.

## Endpoints da API

A API de Tarefas oferece os seguintes endpoints:

- `POST /users`: Cria um novo usuário com senha criptografada. Envie um JSON com as informações do usuário.

- `POST /login`: Realiza login com um usuário existente e retorna um token de acesso JWT.

- `GET /tasks`: Lista todas as tarefas (requer autenticação JWT).

- `POST /tasks`: Cria uma nova tarefa (requer autenticação JWT e privilégios de administrador).

- `PUT /tasks/{task_id}`: Atualiza uma tarefa existente por ID (requer autenticação JWT e privilégios de administrador).

- `DELETE /tasks/{task_id}`: Exclui uma tarefa por ID (requer autenticação JWT e privilégios de administrador).

Lembre-se de que as rotas protegidas (`/tasks`, `/tasks/{task_id}`) exigem autenticação JWT e privilégios de administrador. Você pode personalizar essas configurações conforme necessário.

## Contribuições

Este projeto está aberto a contribuições. Se você deseja melhorar, corrigir bugs ou adicionar novos recursos, sinta-se à vontade para criar um fork deste repositório, fazer suas alterações e enviar um pull request.

---

Este README fornece uma visão geral detalhada da API de Tarefas, orientações sobre configuração, instalação e uso, além de informações sobre o banco de dados utilizado. Lembre-se de personalizar o README com informações adicionais ou requisitos específicos do seu projeto, se aplicável.
