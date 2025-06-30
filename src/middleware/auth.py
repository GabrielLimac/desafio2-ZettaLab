"""
Middleware e utilitários de autenticação
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.auth_service import AuthService

def auth_required(f):
    """
    Decorator para rotas que requerem autenticação
    Combina jwt_required com verificação de usuário válido
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            user = AuthService.get_user_by_id(current_user_id)
            
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
            
            # Adicionar usuário ao contexto da função
            return f(current_user=user, *args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': f'Erro de autenticação: {str(e)}'}), 500
    
    return decorated_function

def get_current_user():
    """
    Obter usuário atual autenticado
    
    Returns:
        User|None: Usuário autenticado ou None
    """
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            return AuthService.get_user_by_id(current_user_id)
        return None
    except Exception:
        return None

def validate_request_data(required_fields):
    """
    Decorator para validar dados obrigatórios na requisição
    
    Args:
        required_fields (list): Lista de campos obrigatórios
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Dados não fornecidos'}), 400
            
            missing_fields = []
            for field in required_fields:
                if field not in data or not data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                return jsonify({
                    'error': f'Campos obrigatórios ausentes: {", ".join(missing_fields)}'
                }), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

