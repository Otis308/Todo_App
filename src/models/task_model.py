import uuid
from datetime import datetime

class Task:
    def __init__(self, title, description="", priority="Thấp", deadline=None, status="Đang chờ", category="All Tasks", completed=False, task_id=None, created_date=None, source="manual"):
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.category = category
        self.created_date = created_date or datetime.now().strftime("%d/%m/%Y")
        self.source = source
        self.deadline = deadline or ""
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
            "deadline": self.deadline,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "Thấp"),
            deadline=data.get("deadline", ""),
            status=data.get("status", "Đang chờ"),
            category=data.get("category", "All Tasks"),
            completed=data.get("completed", False),
            task_id=data.get("task_id"),
            created_date=data.get("created_date"),
            source=data.get("source", "manual")
        )