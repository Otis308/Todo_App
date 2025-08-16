from src.models.task_model import Task

class TaskService:
    def __init__(self, task_repo, user_email):
        self.task_repo = task_repo
        self.user_email = user_email

    def create_task(self, title, description="", priority="Thấp", status="Đang chờ", category="All Tasks", completed=False):
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            category=category,
            completed=completed
        )
        self.task_repo.add_task(self.user_email, task)
        return task

    def get_task(self, task_id):
        tasks = self.task_repo.load_tasks(self.user_email)
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None

    def update_task(self, task_id, **kwargs):
        tasks = self.task_repo.load_tasks(self.user_email)
        for idx, task in enumerate(tasks):
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.task_repo.save_tasks(self.user_email, tasks)
                return task
        return None

    def delete_task(self, task_id):
        self.task_repo.delete_task(self.user_email, task_id)

    def list_tasks(self):
        return self.task_repo.load_tasks(self.user_email)