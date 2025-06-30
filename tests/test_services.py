"""
Testes para os serviços da API de Tarefas
"""

import pytest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db, User, Task
from src.services.auth_service import AuthService
from src.services.task_service import TaskService
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
def app_context(app):
    """Contexto da aplicação"""
    with app.app_context():
        yield app

class TestAuthService:
    """Testes para o serviço de autenticação"""
    
    def test_validate_email(self):
        """Testar validação de email"""
        assert AuthService.validate_email("teste@exemplo.com") is True
        assert AuthService.validate_email("email_invalido") is False
        assert AuthService.validate_email("") is False
        assert AuthService.validate_email("teste@") is False
    
    def test_validate_password(self):
        """Testar validação de senha"""
        is_valid, message = AuthService.validate_password("123456")
        assert is_valid is True
        
        is_valid, message = AuthService.validate_password("123")
        assert is_valid is False
        assert "pelo menos 6 caracteres" in message
    
    def test_register_user_success(self, app_context):
        """Testar registro de usuário com sucesso"""
        success, message, user = AuthService.register_user(
            "João Silva",
            "joao@exemplo.com",
            "senha123"
        )
        
        assert success is True
        assert "criado com sucesso" in message
        assert user is not None
        assert user.name == "João Silva"
        assert user.email == "joao@exemplo.com"
    
    def test_register_user_duplicate_email(self, app_context):
        """Testar registro com email duplicado"""
        # Primeiro registro
        AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Segundo registro com mesmo email
        success, message, user = AuthService.register_user(
            "Maria",
            "joao@exemplo.com",
            "senha456"
        )
        
        assert success is False
        assert "já cadastrado" in message
        assert user is None
    
    def test_register_user_invalid_data(self, app_context):
        """Testar registro com dados inválidos"""
        # Nome vazio
        success, message, user = AuthService.register_user("", "email@teste.com", "senha123")
        assert success is False
        assert "obrigatório" in message
        
        # Email inválido
        success, message, user = AuthService.register_user("Nome", "email_invalido", "senha123")
        assert success is False
        assert "inválido" in message
        
        # Senha muito curta
        success, message, user = AuthService.register_user("Nome", "email@teste.com", "123")
        assert success is False
        assert "6 caracteres" in message
    
    def test_authenticate_user_success(self, app_context):
        """Testar autenticação com sucesso"""
        # Registrar usuário primeiro
        AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Autenticar
        success, message, tokens = AuthService.authenticate_user("joao@exemplo.com", "senha123")
        
        assert success is True
        assert "sucesso" in message
        assert tokens is not None
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert 'user' in tokens
    
    def test_authenticate_user_invalid_credentials(self, app_context):
        """Testar autenticação com credenciais inválidas"""
        # Registrar usuário primeiro
        AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Tentar autenticar com senha errada
        success, message, tokens = AuthService.authenticate_user("joao@exemplo.com", "senha_errada")
        
        assert success is False
        assert "incorretos" in message
        assert tokens is None
    
    def test_get_user_by_id(self, app_context):
        """Testar busca de usuário por ID"""
        # Registrar usuário
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Buscar por ID
        found_user = AuthService.get_user_by_id(user.id)
        
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email

class TestTaskService:
    """Testes para o serviço de tarefas"""
    
    def test_validate_task_data(self):
        """Testar validação de dados da tarefa"""
        # Dados válidos
        is_valid, message = TaskService.validate_task_data("Tarefa Teste", "Descrição", "pendente")
        assert is_valid is True
        
        # Nome vazio
        is_valid, message = TaskService.validate_task_data("", "Descrição", "pendente")
        assert is_valid is False
        assert "obrigatório" in message
        
        # Status inválido
        is_valid, message = TaskService.validate_task_data("Tarefa", "Descrição", "status_invalido")
        assert is_valid is False
        assert "Status deve ser" in message
    
    def test_create_task_success(self, app_context):
        """Testar criação de tarefa com sucesso"""
        # Criar usuário primeiro
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Criar tarefa
        success, message, task = TaskService.create_task(
            user.id,
            "Tarefa Teste",
            "Descrição da tarefa",
            "pendente"
        )
        
        assert success is True
        assert "criada com sucesso" in message
        assert task is not None
        assert task.name == "Tarefa Teste"
        assert task.user_id == user.id
    
    def test_get_user_tasks(self, app_context):
        """Testar busca de tarefas do usuário"""
        # Criar usuário
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Criar tarefas
        TaskService.create_task(user.id, "Tarefa 1", "Descrição 1", "pendente")
        TaskService.create_task(user.id, "Tarefa 2", "Descrição 2", "concluida")
        TaskService.create_task(user.id, "Tarefa 3", "Descrição 3", "pendente")
        
        # Buscar todas as tarefas
        success, message, data = TaskService.get_user_tasks(user.id)
        
        assert success is True
        assert len(data['tasks']) == 3
        
        # Buscar apenas pendentes
        success, message, data = TaskService.get_user_tasks(user.id, status="pendente")
        
        assert success is True
        assert len(data['tasks']) == 2
        
        # Buscar apenas concluídas
        success, message, data = TaskService.get_user_tasks(user.id, status="concluida")
        
        assert success is True
        assert len(data['tasks']) == 1
    
    def test_update_task(self, app_context):
        """Testar atualização de tarefa"""
        # Criar usuário e tarefa
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        success, message, task = TaskService.create_task(user.id, "Tarefa Original", "Descrição", "pendente")
        
        # Atualizar tarefa
        success, message, updated_task = TaskService.update_task(
            task.id,
            user.id,
            name="Tarefa Atualizada",
            status="concluida"
        )
        
        assert success is True
        assert "atualizada com sucesso" in message
        assert updated_task.name == "Tarefa Atualizada"
        assert updated_task.status == "concluida"
    
    def test_delete_task(self, app_context):
        """Testar exclusão de tarefa"""
        # Criar usuário e tarefa
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        success, message, task = TaskService.create_task(user.id, "Tarefa para Deletar", "Descrição", "pendente")
        
        # Deletar tarefa
        success, message = TaskService.delete_task(task.id, user.id)
        
        assert success is True
        assert "excluída com sucesso" in message
        
        # Verificar se foi deletada
        success, message, found_task = TaskService.get_task_by_id(task.id, user.id)
        assert success is False
        assert "não encontrada" in message
    
    def test_get_task_statistics(self, app_context):
        """Testar estatísticas das tarefas"""
        # Criar usuário
        success, message, user = AuthService.register_user("João", "joao@exemplo.com", "senha123")
        
        # Criar tarefas
        TaskService.create_task(user.id, "Tarefa 1", "Descrição", "pendente")
        TaskService.create_task(user.id, "Tarefa 2", "Descrição", "pendente")
        TaskService.create_task(user.id, "Tarefa 3", "Descrição", "concluida")
        
        # Obter estatísticas
        success, message, stats = TaskService.get_task_statistics(user.id)
        
        assert success is True
        assert stats['total'] == 3
        assert stats['pendente'] == 2
        assert stats['concluida'] == 1
        assert stats['completion_rate'] == 33.33

