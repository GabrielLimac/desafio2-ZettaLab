import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.config import config
from src.models import db
from src.routes.user import user_bp
from src.routes.task import task_bp

def create_app(config_name=None):
    """função para criar a aplicação Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(task_bp, url_prefix='/api')
    
    with app.app_context():
        # Criar diretório do banco se não existir
        db_path = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        db.create_all()
    
    # Rota para servir arquivos estáticos (frontend)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder não configurada", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return {"message": "API de Gerenciamento de Tarefas", "version": "1.1"}, 200
    
    # Erros JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token expirado"}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "Token inválido"}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"message": "Token de autorização necessário"}, 401
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

