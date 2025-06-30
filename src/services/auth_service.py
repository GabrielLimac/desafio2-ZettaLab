"""
Serviço de autenticação para a API de Tarefas
"""

from flask_jwt_extended import create_access_token, create_refresh_token
from src.models import db, User
import re

class AuthService:
    """Serviço responsável pela autenticação de usuários"""
    
    @staticmethod
    def validate_email(email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Valida se a senha atende aos critérios mínimos"""
        if len(password) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres"
        return True, "Senha válida"
    
    @staticmethod
    def register_user(name, email, password):
        """
        Registra um novo usuário
        
        Args:
            name (str): Nome do usuário
            email (str): Email do usuário
            password (str): Senha do usuário
            
        Returns:
            tuple: (success: bool, message: str, user: User|None)
        """
        try:
            # Validar dados de entrada
            if not name or not name.strip():
                return False, "Nome é obrigatório", None
            
            if not email or not email.strip():
                return False, "Email é obrigatório", None
            
            if not AuthService.validate_email(email):
                return False, "Formato de email inválido", None
            
            is_valid_password, password_message = AuthService.validate_password(password)
            if not is_valid_password:
                return False, password_message, None
            
            # Verificar se email já existe
            existing_user = User.query.filter_by(email=email.lower().strip()).first()
            if existing_user:
                return False, "Email já cadastrado", None
            
            # Criar novo usuário
            user = User(
                name=name.strip(),
                email=email.lower().strip()
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return True, "Usuário criado com sucesso", user
            
        except Exception as e:
            db.session.rollback()
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Autentica um usuário
        
        Args:
            email (str): Email do usuário
            password (str): Senha do usuário
            
        Returns:
            tuple: (success: bool, message: str, tokens: dict|None)
        """
        try:
            if not email or not password:
                return False, "Email e senha são obrigatórios", None
            
            # Buscar usuário pelo email
            user = User.query.filter_by(email=email.lower().strip()).first()
            
            if not user or not user.check_password(password):
                return False, "Email ou senha incorretos", None
            
            # Gerar tokens JWT
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            tokens = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
            
            return True, "Login realizado com sucesso", tokens
            
        except Exception as e:
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Busca usuário por ID
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            User|None: Usuário encontrado ou None
        """
        try:
            return User.query.get(user_id)
        except Exception:
            return None

