import uuid
from datetime import datetime

class Task:
    def __init__(self, title, description="", priority="Thấp", status="Đang chờ", category="All Tasks", completed=False):
        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.category = category
        self.created_date = datetime.now().strftime("%d/%m/%Y")
        self.source = "manual"
        self.completed = completed

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "category": self.category,
            "created_date": self.created_date,
            "source": self.source,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data: dict):
        task = Task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "Thấp"),
            status=data.get("status", "Đang chờ"),
            category=data.get("category", "All Tasks"),
            completed=data.get("completed", False)
        )
        task.task_id = data.get("task_id", str(uuid.uuid4()))
        task.created_date = data.get("created_date", datetime.now().strftime("%d/%m/%Y"))
        task.source = data.get("source", "manual")
        return task