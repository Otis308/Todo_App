from models.task_model import Task

class TaskService:
    def __init__(self, task_repo, user_email):
        self.task_repo = task_repo
        self.user_email = user_email

    def create_task(self, title, description="", priority="Thấp", status="Đang chờ", category="All Tasks", deadline=None, completed=False):
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            category=category,
            deadline=deadline,
            completed=completed,
            source="manual"
        )
        self.task_repo.add_task(self.user_email, task)
        return task

    def get_task(self, task_id):
        tasks = self.task_repo.load_tasks(self.user_email)
        for t in tasks:
            if t.task_id == task_id:
                return t
        return None

    def update_task(self, task_id, **kwargs):
        tasks = self.task_repo.load_tasks(self.user_email)
        for t in tasks:
            if t.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(t, key):
                        setattr(t, key, value)
                self.task_repo.update_task(self.user_email, t)
                return t
        return None

    def delete_task(self, task_id):
        tasks = self.task_repo.load_tasks(self.user_email)
        tasks = [t for t in tasks if t.task_id != task_id]
        self.task_repo.save_tasks(self.user_email, tasks)

    def list_tasks(self):
        return self.task_repo.load_tasks(self.user_email)