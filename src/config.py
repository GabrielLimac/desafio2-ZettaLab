import os
from datetime import timedelta

class Config:
    """Configurações"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-de-producao'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-chave-de-producao'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_CSRF_IN_COOKIES = False
    JWT_ACCESS_CSRF_HEADER_NAME = None
    JWT_REFRESH_CSRF_HEADER_NAME = None
    JWT_CSRF_METHODS = []
    
    # Configurações CORS
    CORS_ORIGINS = ["*"]

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

