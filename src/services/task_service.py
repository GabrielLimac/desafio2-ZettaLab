"""
Serviço de gerenciamento de tarefas
"""

from src.models import db, Task, User
from sqlalchemy import and_

class TaskService:
    """Serviço responsável pelo gerenciamento de tarefas"""
    
    VALID_STATUSES = ['pendente', 'concluida']
    
    @staticmethod
    def validate_task_data(name, description=None, status=None):
        """
        Valida dados da tarefa
        
        Args:
            name (str): Nome da tarefa
            description (str): Descrição da tarefa
            status (str): Status da tarefa
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        if not name or not name.strip():
            return False, "Nome da tarefa é obrigatório"
        
        if len(name.strip()) > 200:
            return False, "Nome da tarefa deve ter no máximo 200 caracteres"
        
        if description and len(description) > 1000:
            return False, "Descrição deve ter no máximo 1000 caracteres"
        
        if status and status not in TaskService.VALID_STATUSES:
            return False, f"Status deve ser um dos seguintes: {', '.join(TaskService.VALID_STATUSES)}"
        
        return True, "Dados válidos"
    
    @staticmethod
    def create_task(user_id, name, description=None, status='pendente'):
        """
        Criar nova tarefa
        
        Args:
            user_id (int): ID do usuário
            name (str): Nome da tarefa
            description (str): Descrição da tarefa
            status (str): Status da tarefa
            
        Returns:
            tuple: (success: bool, message: str, task: Task|None)
        """
        try:
            # Validar dados
            is_valid, message = TaskService.validate_task_data(name, description, status)
            if not is_valid:
                return False, message, None
            
            # Verificar se usuário existe
            user = User.query.get(user_id)
            if not user:
                return False, "Usuário não encontrado", None
            
            # Criar tarefa
            task = Task(
                name=name.strip(),
                description=description.strip() if description else None,
                status=status,
                user_id=user_id
            )
            
            db.session.add(task)
            db.session.commit()
            
            return True, "Tarefa criada com sucesso", task
            
        except Exception as e:
            db.session.rollback()
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def get_user_tasks(user_id, status=None, page=1, per_page=20):
        """
        Obter tarefas do usuário
        
        Args:
            user_id (int): ID do usuário
            status (str): Filtro por status (opcional)
            page (int): Página para paginação
            per_page (int): Itens por página
            
        Returns:
            tuple: (success: bool, message: str, data: dict|None)
        """
        try:
            # Construir query base
            query = Task.query.filter_by(user_id=user_id)
            
            # Aplicar filtro de status se fornecido
            if status:
                if status not in TaskService.VALID_STATUSES:
                    return False, f"Status inválido. Use: {', '.join(TaskService.VALID_STATUSES)}", None
                query = query.filter_by(status=status)
            
            # Ordenar por data de criação (mais recentes primeiro)
            query = query.order_by(Task.created_at.desc())
            
            # Aplicar paginação
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            tasks = [task.to_dict() for task in pagination.items]
            
            data = {
                'tasks': tasks,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
            return True, "Tarefas obtidas com sucesso", data
            
        except Exception as e:
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def get_task_by_id(task_id, user_id):
        """
        Obter tarefa por ID (verificando se pertence ao usuário)
        
        Args:
            task_id (int): ID da tarefa
            user_id (int): ID do usuário
            
        Returns:
            tuple: (success: bool, message: str, task: Task|None)
        """
        try:
            task = Task.query.filter(
                and_(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if not task:
                return False, "Tarefa não encontrada", None
            
            return True, "Tarefa encontrada", task
            
        except Exception as e:
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def update_task(task_id, user_id, name=None, description=None, status=None):
        """
        Atualizar tarefa
        
        Args:
            task_id (int): ID da tarefa
            user_id (int): ID do usuário
            name (str): Novo nome da tarefa
            description (str): Nova descrição da tarefa
            status (str): Novo status da tarefa
            
        Returns:
            tuple: (success: bool, message: str, task: Task|None)
        """
        try:
            # Buscar tarefa
            success, message, task = TaskService.get_task_by_id(task_id, user_id)
            if not success:
                return success, message, task
            
            # Validar novos dados se fornecidos
            if name is not None:
                is_valid, validation_message = TaskService.validate_task_data(name, description, status)
                if not is_valid:
                    return False, validation_message, None
                task.name = name.strip()
            
            if description is not None:
                if description and len(description) > 1000:
                    return False, "Descrição deve ter no máximo 1000 caracteres", None
                task.description = description.strip() if description else None
            
            if status is not None:
                if status not in TaskService.VALID_STATUSES:
                    return False, f"Status deve ser um dos seguintes: {', '.join(TaskService.VALID_STATUSES)}", None
                task.status = status
            
            db.session.commit()
            
            return True, "Tarefa atualizada com sucesso", task
            
        except Exception as e:
            db.session.rollback()
            return False, f"Erro interno: {str(e)}", None
    
    @staticmethod
    def delete_task(task_id, user_id):
        """
        Excluir tarefa
        
        Args:
            task_id (int): ID da tarefa
            user_id (int): ID do usuário
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Buscar tarefa
            success, message, task = TaskService.get_task_by_id(task_id, user_id)
            if not success:
                return success, message
            
            db.session.delete(task)
            db.session.commit()
            
            return True, "Tarefa excluída com sucesso"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Erro interno: {str(e)}"
    
    @staticmethod
    def get_task_statistics(user_id):
        """
        Obter estatísticas das tarefas do usuário
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            tuple: (success: bool, message: str, stats: dict|None)
        """
        try:
            total_tasks = Task.query.filter_by(user_id=user_id).count()
            pending_tasks = Task.query.filter_by(user_id=user_id, status='pendente').count()
            completed_tasks = Task.query.filter_by(user_id=user_id, status='concluida').count()
            
            stats = {
                'total': total_tasks,
                'pendente': pending_tasks,
                'concluida': completed_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
            }
            
            return True, "Estatísticas obtidas com sucesso", stats
            
        except Exception as e:
            return False, f"Erro interno: {str(e)}", None

