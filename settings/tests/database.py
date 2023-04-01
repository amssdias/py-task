import sqlite3
from settings.database.database import DatabaseConnection
from settings.database.utils import create_tables_database


class TestDatabaseConnection(DatabaseConnection):
    database_path = "test.db"

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = self.row_factory
        return self.connection
