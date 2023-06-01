from typing import Dict, Optional
from apps.accounts.constants.database import DB_COLUMNS

from apps.accounts.utils.password import Password
from settings.database import DatabaseConnection
from settings.settings import DATABASE_PATH


class Users:

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        self.database = DatabaseConnection
        self.columns = DB_COLUMNS

    def create_user(self, email: str, password: str) -> bool:
        hashed_password = Password.hash_password(password)
        try:
            with self.database(self.database_path) as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users(email, password) VALUES(?, ?)", (email, hashed_password))
        except Exception as e:
            # TODO: Add log
            return False
        return True

    def update(self, email: str, new_values: Dict) -> bool:
        user = self.get_user(email)
        if not user:
            return False

        try:
            with self.database(self.database_path) as connection:
                cursor = connection.cursor()
                for key, value in new_values.items():
                    if key == "password":
                        value = Password.hash_password(value)
                    query = f"UPDATE users SET {key} = ? WHERE user_id = ?"
                    cursor.execute(query, (value, user["user_id"]))
        except Exception as e:
            # TODO: Add log
            return False
        return True

    def get_user(self, email: str) -> Optional[Dict]:
        try:
            with self.database(self.database_path) as connection:
                cursor = connection.cursor()
                query = f"SELECT {', '.join(self.columns)} FROM users WHERE email = ?"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
        except Exception as e:
            # TODO: Add log
            return None
        return dict(user) if user else None
