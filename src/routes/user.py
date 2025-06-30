"""
Rotas de autenticação e usuário
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.services.auth_service import AuthService

# Criar blueprint para rotas de usuário/autenticação
user_bp = Blueprint('auth', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        success, message, user = AuthService.register_user(name, email, password)
        
        if success:
            return jsonify({
                'message': message,
                'user': user.to_dict()
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Fazer login do usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        success, message, tokens = AuthService.authenticate_user(email, password)
        
        if success:
            return jsonify({
                'message': message,
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'user': tokens['user']
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar token de acesso"""
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'message': 'Token renovado com sucesso',
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obter perfil do usuário autenticado"""
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualizar perfil do usuário autenticado"""
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Atualizar nome se fornecido
        if 'name' in data and data['name'].strip():
            user.name = data['name'].strip()
        
        # Atualizar email se fornecido
        if 'email' in data:
            new_email = data['email'].lower().strip()
            if new_email != user.email:
                if not AuthService.validate_email(new_email):
                    return jsonify({'error': 'Formato de email inválido'}), 400
                
                # Verificar se novo email já existe
                from src.models import User
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    return jsonify({'error': 'Email já está em uso'}), 400
                
                user.email = new_email
        
        # Atualizar senha se fornecida
        if 'password' in data:
            is_valid, message = AuthService.validate_password(data['password'])
            if not is_valid:
                return jsonify({'error': message}), 400
            user.set_password(data['password'])
        
        from src.models import db
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        from src.models import db
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

# Rota de teste para verificar se a API está funcionando
@user_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'API de Gerenciamento de Tarefas está funcionando',
        'version': '1.1'
    }), 200

