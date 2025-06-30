"""
Rotas para gerenciamento de tarefas
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.task_service import TaskService
from src.services.auth_service import AuthService

# Criar blueprint para rotas de tarefas
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Criar nova tarefa"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name')
        description = data.get('description')
        status = data.get('status', 'pendente')
        
        success, message, task = TaskService.create_task(
            user_id=current_user_id,
            name=name,
            description=description,
            status=status
        )
        
        if success:
            return jsonify({
                'message': message,
                'task': task.to_dict()
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Listar tarefas do usuário com filtros opcionais"""
    try:
        current_user_id = get_jwt_identity()
        
        # Parâmetros de query
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Máximo 100 por página
        
        success, message, data = TaskService.get_user_tasks(
            user_id=current_user_id,
            status=status,
            page=page,
            per_page=per_page
        )
        
        if success:
            return jsonify({
                'message': message,
                **data
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except ValueError:
        return jsonify({'error': 'Parâmetros de paginação inválidos'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Obter tarefa específica"""
    try:
        current_user_id = get_jwt_identity()
        
        success, message, task = TaskService.get_task_by_id(task_id, current_user_id)
        
        if success:
            return jsonify({
                'message': message,
                'task': task.to_dict()
            }), 200
        else:
            return jsonify({'error': message}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Atualizar tarefa"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name')
        description = data.get('description')
        status = data.get('status')
        
        success, message, task = TaskService.update_task(
            task_id=task_id,
            user_id=current_user_id,
            name=name,
            description=description,
            status=status
        )
        
        if success:
            return jsonify({
                'message': message,
                'task': task.to_dict()
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Excluir tarefa"""
    try:
        current_user_id = get_jwt_identity()
        
        success, message = TaskService.delete_task(task_id, current_user_id)
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks/stats', methods=['GET'])
@jwt_required()
def get_task_statistics():
    """Obter estatísticas das tarefas do usuário"""
    try:
        current_user_id = get_jwt_identity()
        
        success, message, stats = TaskService.get_task_statistics(current_user_id)
        
        if success:
            return jsonify({
                'message': message,
                'statistics': stats
            }), 200
        else:
            return jsonify({'error': message}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

# Rotas para filtros específicos (conveniência)
@task_bp.route('/tasks/pending', methods=['GET'])
@jwt_required()
def get_pending_tasks():
    """Listar apenas tarefas pendentes"""
    try:
        current_user_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        
        success, message, data = TaskService.get_user_tasks(
            user_id=current_user_id,
            status='pendente',
            page=page,
            per_page=per_page
        )
        
        if success:
            return jsonify({
                'message': message,
                **data
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except ValueError:
        return jsonify({'error': 'Parâmetros de paginação inválidos'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@task_bp.route('/tasks/completed', methods=['GET'])
@jwt_required()
def get_completed_tasks():
    """Listar apenas tarefas concluídas"""
    try:
        current_user_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        
        success, message, data = TaskService.get_user_tasks(
            user_id=current_user_id,
            status='concluida',
            page=page,
            per_page=per_page
        )
        
        if success:
            return jsonify({
                'message': message,
                **data
            }), 200
        else:
            return jsonify({'error': message}), 400
            
    except ValueError:
        return jsonify({'error': 'Parâmetros de paginação inválidos'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

