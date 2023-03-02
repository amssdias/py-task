from typing import Dict, Optional
from apps.accounts.utils.password import Password
from settings.database import Database


class Users:

    def __init__(self):
        self.database = Database()

    def create_user(self, email: str, password: str) -> bool:
        hashed_password = Password.hash_password(password)
        self.database["users"].append({"email": email, "password": hashed_password})
        return True

    def update(self, email, password):
        pass

    def reset_password(self, email):
        pass

    def get_user(self, email: str) -> Optional[Dict]:
        for user in self.database["users"]:
            if user["email"] == email:
                return user
        return None