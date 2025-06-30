"""
Testes para os modelos da API de Tarefas
"""

import pytest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, User, Task
from src.config import config
from flask import Flask

@pytest.fixture
def app():
    """Criar aplicação Flask para testes"""
    app = Flask(__name__)
    app.config.from_object(config['testing'])
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Contexto da aplicação"""
    with app.app_context():
        yield app

class TestUserModel:
    """Testes para o modelo User"""
    
    def test_create_user(self, app_context):
        """Testar criação de usuário"""
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.name == "Teste"
        assert user.email == "teste@exemplo.com"
        assert user.password_hash is not None
        assert user.password_hash != "123456"  # Senha deve estar hasheada
    
    def test_check_password(self, app_context):
        """Testar verificação de senha"""
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        
        assert user.check_password("123456") is True
        assert user.check_password("senha_errada") is False
    
    def test_user_to_dict(self, app_context):
        """Testar conversão para dicionário"""
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        
        assert 'id' in user_dict
        assert 'name' in user_dict
        assert 'email' in user_dict
        assert 'created_at' in user_dict
        assert 'updated_at' in user_dict
        assert 'password_hash' not in user_dict  # Senha não deve aparecer

class TestTaskModel:
    """Testes para o modelo Task"""
    
    def test_create_task(self, app_context):
        """Testar criação de tarefa"""
        # Criar usuário primeiro
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        
        # Criar tarefa
        task = Task(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pendente",
            user_id=user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        assert task.id is not None
        assert task.name == "Tarefa Teste"
        assert task.description == "Descrição da tarefa"
        assert task.status == "pendente"
        assert task.user_id == user.id
    
    def test_task_to_dict(self, app_context):
        """Testar conversão para dicionário"""
        # Criar usuário primeiro
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        
        # Criar tarefa
        task = Task(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pendente",
            user_id=user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        task_dict = task.to_dict()
        
        assert 'id' in task_dict
        assert 'name' in task_dict
        assert 'description' in task_dict
        assert 'status' in task_dict
        assert 'user_id' in task_dict
        assert 'created_at' in task_dict
        assert 'updated_at' in task_dict
    
    def test_user_task_relationship(self, app_context):
        """Testar relacionamento entre usuário e tarefas"""
        # Criar usuário
        user = User(name="Teste", email="teste@exemplo.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        
        # Criar tarefas
        task1 = Task(name="Tarefa 1", status="pendente", user_id=user.id)
        task2 = Task(name="Tarefa 2", status="concluida", user_id=user.id)
        
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()
        
        # Verificar relacionamento
        assert len(user.tasks) == 2
        assert task1 in user.tasks
        assert task2 in user.tasks
        assert task1.user == user
        assert task2.user == user

