"""
Script para inicializar o banco de dados da API de Tarefas
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.config import config
from src.models import db, User, Task

def create_app(config_name='development'):
    """Criar aplicação Flask com configuração específica"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    
    return app

def init_database():
    """Inicializar o banco de dados"""
    app = create_app()
    
    with app.app_context():
        # Criar diretório do banco se não existir
        db_path = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        # Criar todas as tabelas
        db.create_all()
        print("Banco de dados inicializado com sucesso!")
        print(f"Localização: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Verificar se as tabelas foram criadas
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas criadas: {', '.join(tables)}")

def create_sample_data():
    """Criar dados de exemplo (opcional)"""
    app = create_app()
    
    with app.app_context():
        # Verificar se já existem usuários
        if User.query.first():
            print("Dados já existem no banco. Pulando criação de dados de exemplo.")
            return
        
        # Criar usuário de exemplo
        user = User(name="Usuário Teste", email="teste@exemplo.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        
        # Criar tarefas de exemplo
        tasks = [
            Task(name="Estudar Flask", description="Aprender sobre desenvolvimento de APIs com Flask", status="pendente", user_id=user.id),
            Task(name="Implementar autenticação", description="Adicionar sistema de login com JWT", status="concluida", user_id=user.id),
            Task(name="Escrever testes", description="Criar testes unitários para a API", status="pendente", user_id=user.id)
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        print("Dados de exemplo criados!")
        print(f"Usuário: {user.email} (senha: 123456)")
        print(f"{len(tasks)} tarefas criadas")

if __name__ == '__main__':
    print("Inicializando banco de dados da API de Tarefas...")
    init_database()
    
    # Perguntar se deve criar dados de exemplo
    create_sample = input("\n Deseja criar dados de exemplo? (s/N): ").lower().strip()
    if create_sample in ['s', 'sim', 'y', 'yes']:
        create_sample_data()
    
    print("\n Configuração concluída!")

