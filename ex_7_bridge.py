from flask import Flask, jsonify, request
from peewee import Model, CharField, BooleanField, PostgresqlDatabase, IntegrityError
from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import bcrypt
from functools import wraps
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

# Configuração do banco de dados PostgreSQL
db = PostgresqlDatabase('postgres', user='postgres', password='AG123', host='localhost', port=5432)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = '123'
jwt = JWTManager(app)

# Definição do modelo Peewee para a tabela 'tasks'
class Task(Model):
    title = CharField()
    completed = BooleanField()

    class Meta:
        database = db

# Definição do modelo Peewee para a tabela 'users'
class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    admin = BooleanField(default=False)
    auth_token = CharField(null=True)

    class Meta:
        database = db

# Inicialização do banco de dados e criação das tabelas (caso não existam)
db.connect()
db.create_tables([Task, User], safe=True)

# Inserção de tarefas iniciais (caso não existam)
initial_tasks = [
    {"title": "Fazer compras", "completed": False},
    {"title": "Estudar para a prova", "completed": True},
]

for task_data in initial_tasks:
    try:
        Task.create(**task_data)
    except IntegrityError:
        pass

# Função de decoração personalizada para verificar se o usuário é um administrador
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.get(User.username == current_user)
        if user.admin:
            return fn(*args, **kwargs)
        abort(403, message="Acesso não autorizado para esta rota")  # Aborta a solicitação com código 403 (Proibido)
    return wrapper

# Rota para criar um novo usuário com senha criptografada
class CreateUserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        admin = data.get('admin', False)  # Se não for fornecido, assume como False

        # Criptografa a senha antes de armazená-la no banco de dados
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            user = User.create(username=username, email=email, password=hashed_password, admin=admin)
            return {"message": "Usuário criado com sucesso"}, 201
        except IntegrityError:
            abort(400, message="Erro ao criar usuário. Verifique os dados de entrada")  # Aborta a solicitação com código 400 (Bad Request)

# Rota de login
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        try:
            user = User.get((User.username == username_or_email) | (User.email == username_or_email))
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                expires = timedelta(minutes=20)  # Define o tempo de expiração para 20 minutos
                access_token = create_access_token(identity=user.username, expires_delta=expires, user_claims={"admin": user.admin})
                user.auth_token = access_token
                user.save()
                return {"message": "Login bem-sucedido", "access_token": access_token}, 200
        except User.DoesNotExist:
            pass

        abort(401, message="Credenciais inválidas")  # Aborta a solicitação com código 401 (Não Autorizado)

# Rota protegida com autenticação JWT e política de acesso para obter todas as tarefas
class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        tasks = Task.select()
        task_list = [model_to_dict(task) for task in tasks]
        return {"tasks": task_list}

# Rota protegida com autenticação JWT e política de acesso para criar uma nova tarefa (apenas administradores)
class CreateTaskResource(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        new_task_data = request.json
        try:
            new_task = Task.create(**new_task_data)
            return {"message": "Tarefa criada com sucesso", "task": model_to_dict(new_task)}, 201
        except IntegrityError:
            abort(400, message="Erro ao criar tarefa. Verifique os dados de entrada")  # Aborta a solicitação com código 400 (Bad Request)

# Rota protegida com autenticação JWT e política de acesso para atualizar uma tarefa existente por ID (apenas administradores)
class UpdateTaskResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, task_id):
        try:
            task = Task.get(Task.id == task_id)
            task_data = request.json
            task.title = task_data.get("title", task.title)
            task.completed = task_data.get("completed", task.completed)
            task.save()
            return {"message": "Tarefa atualizada com sucesso"}
        except Task.DoesNotExist:
            abort(404, message="Tarefa não encontrada")  # Aborta a solicitação com código 404 (Não Encontrado)

# Rota protegida com autenticação JWT e política de acesso para excluir uma tarefa por ID (apenas administradores)
class DeleteTaskResource(Resource):
    @jwt_required()
    @admin_required
    def delete(self, task_id):
        try:
            task = Task.get(Task.id == task_id)
            task.delete_instance()
            return {"message": "Tarefa excluída com sucesso"}
        except Task.DoesNotExist:
            abort(404, message="Tarefa não encontrada")  # Aborta a solicitação com código 404 (Não Encontrado)

# Adiciona as rotas à API
api.add_resource(CreateUserResource, '/users')
api.add_resource(LoginResource, '/login')
api.add_resource(TaskListResource, '/tasks')
api.add_resource(CreateTaskResource, '/tasks')
api.add_resource(UpdateTaskResource, '/tasks/<int:task_id>')
api.add_resource(DeleteTaskResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
