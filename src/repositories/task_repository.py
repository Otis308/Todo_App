import os
import json
from src.models.task_model import Task
from src.config import TASKS_DIR

class TaskRepository:
    def __init__(self):
        if not os.path.exists(TASKS_DIR):
            os.makedirs(TASKS_DIR)

    def _get_file_path(self, user_email: str):
        safe_email = user_email.replace("@", "_at_").replace(".", "_dot_")
        return os.path.join(TASKS_DIR, f"{safe_email}.json")

    def load_tasks(self, user_email: str):
        file_path = self._get_file_path(user_email)
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(t) for t in data]

    def save_tasks(self, user_email: str, tasks):
        file_path = self._get_file_path(user_email)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)

    def add_task(self, user_email: str, task: Task):
        tasks = self.load_tasks(user_email)
        tasks.append(task)
        self.save_tasks(user_email, tasks)

    def update_task(self, user_email: str, task: Task):
        tasks = self.load_tasks(user_email)
        for idx, t in enumerate(tasks):
            if t.task_id == task.task_id:
                tasks[idx] = task
                break
        self.save_tasks(user_email, tasks)

    def delete_task(self, user_email: str, task_id: str):
        tasks = self.load_tasks(user_email)
        tasks = [t for t in tasks if t.task_id != task_id]
        self.save_tasks(user_email, tasks)
