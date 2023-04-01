import sqlite3

from settings.settings import DATABASE_PATH


class DatabaseConnection:
    def __init__(self, path=DATABASE_PATH, row_factory=sqlite3.Row) -> None:
        self.path = path
        self.connection = None
        self.row_factory = row_factory

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = self.row_factory
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.commit()
        self.connection.close()


# In memory initial database
class Database(dict):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self["users"] = []

    def clear(self):
        self["users"] = []


db_instance = Database()


if __name__ == "__main__":
    db = Database()
