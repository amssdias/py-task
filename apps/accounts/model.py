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

    def update(self, email: str, new_values: Dict) -> bool:
        for user in self.database["users"]:
            if user["email"] == email:
                for key, value in new_values.items():
                    if key == "password":
                        user[key] = Password.hash_password(value)
                        continue
                    user[key] = value
                return True
        return False

    def get_user(self, email: str) -> Optional[Dict]:
        for user in self.database["users"]:
            if user["email"] == email:
                return user
        return None