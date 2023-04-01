from settings.database.database import DatabaseConnection
from settings.settings import DATABASE_PATH


def create_tables_database(database_path=DATABASE_PATH) -> None:
    with DatabaseConnection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name VARCHAR(255) NOT NULL,
                task_description TEXT NULL,
                status VARCHAR(12) NOT NULL DEFAULT "Not started" 
                CHECK (status IN ("Not started", "In progress", "Completed", "On hold", "Canceled")),
                priority VARCHAR(1) NOT NULL DEFAULT "M" 
                CHECK (priority IN ("S", "M", "H")),
                due_date DATE NULL,
                user_id INT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL
            );
            """
        )
    return


def dict_factory(cursor, row):
    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
