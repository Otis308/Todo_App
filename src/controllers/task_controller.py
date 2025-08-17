from services.task_service import TaskService
from repositories.task_repository import TaskRepository

class TaskController:
    def __init__(self, user_email):
        self.task_service = TaskService(TaskRepository(), user_email)

    def create_task(self, **kwargs):
        return self.task_service.create_task(**kwargs)

    def get_task(self, task_id):
        return self.task_service.get_task(task_id)

    def update_task(self, task_id, **kwargs):
        return self.task_service.update_task(task_id, **kwargs)

    def delete_task(self, task_id):
        self.task_service.delete_task(task_id)

    def list_tasks(self):
        return self.task_service.list_tasks()