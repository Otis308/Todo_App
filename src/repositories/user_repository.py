import json
import os
from src.config import USERS_FILE
from src.models.user import User
class UserRepository:
    def __init__(self):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_users(self):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def get_user_by_email(self, email):
        users = self.load_users()
        return next((u for u in users if u["email"] == email), None)

    def add_user(self, user: User):
        users = self.load_users()
        users.append(user.to_dict())
        self.save_users(users)
