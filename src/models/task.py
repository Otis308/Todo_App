from tkinter import *
import uuid, os
from datetime import datetime
class User:
    """User class to handle user authentication and data"""
    def __init__(self, username):
        self.username = username
        self.data_dir = os.path.join("data", "users", username)
        self.task_file = os.path.join(self.data_dir, "tasks.json")
        self.ensure_directory()
    
    def ensure_directory(self):
        """Ensure user directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_task_file_path(self):
        """Get path to user's task file"""
        return self.task_file

class Task:
    def __init__(self, title="", description="", due="", priority=2, status="Đang chờ", task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due = due
        self.priority = priority
        self.status = status
        self.completed = (status == "Hoàn thành")
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due": self.due,
            "priority": self.priority,
            "status": self.status,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        task = cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            due=data.get("due", ""),
            priority=data.get("priority", 2),
            status=data.get("status", "Đang chờ"),
            task_id=data.get("id")
        )
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", datetime.now().isoformat())
        return task
