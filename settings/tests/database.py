import sqlite3
from settings.database.database import DatabaseConnection
from settings.settings import TEST_DATABASE_PATH


class TestDatabaseConnection(DatabaseConnection):
    database_path = TEST_DATABASE_PATH

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = self.row_factory
        return self.connection
