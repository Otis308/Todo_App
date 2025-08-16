class User:
    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            password=data["password"]
        )
