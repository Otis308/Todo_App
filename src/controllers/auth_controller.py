from services.auth_service import AuthService
from repositories.user_repository import UserRepository

class AuthController:
    def __init__(self):
        self.user_repository = UserRepository()
        self.auth_service = AuthService(self.user_repository)

    def handle_register(self, name, email, phone, password, confirm_password):
        return self.auth_service.register(name, phone, email, password, confirm_password)

    def handle_login(self, email, password):
        return self.auth_service.login(email, password)
