from typing import Dict, List, Optional
from settings.database import DatabaseConnection
from settings.database.utils import dict_factory
from settings.settings import DATABASE_PATH


class TodoModel:

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        self.database = DatabaseConnection
    
    def create_task(self, user_id, new_task: str) -> bool:
        try:
            with DatabaseConnection() as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO tasks(task_name, user_id) VALUES(?, ?)", (new_task, user_id))
        except Exception as e:
            # TODO: Add log
            return False
        return True

    def update(self, user_id, task_id, new_task: str) -> bool:
        try:
            with DatabaseConnection() as connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE tasks SET task_name = ? WHERE task_id = ? AND user_id = ?", (new_task, task_id, user_id))
        except Exception as e:
            # TODO: Add log
            return False
        return True

    def get_all_tasks(self, user_id, asc=False) -> Optional[List[Dict]]: 
        query = f"""
        SELECT task_id, task_name, task_description, status, priority, due_date, user_id, created_at 
        FROM tasks 
        WHERE user_id = ? 
        ORDER BY created_at {'ASC' if asc else 'DESC'}"""

        try:
            with DatabaseConnection(row_factory=dict_factory) as connection:
                cursor = connection.cursor()
                cursor.execute(query, (user_id, ))
                tasks = cursor.fetchall()
        except Exception as e:
            # TODO: Add log
            return None    
        return tasks if tasks else None
    
    def delete(self, user_id, task_id) -> bool:
        try:
            with DatabaseConnection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tasks WHERE task_id = ? AND user_id = ?", (task_id, user_id))
        except Exception as e:
            # TODO: Add log
            return False
        return True

    def get_task_id(self, user_id, task_id):
        tasks = self.get_all_tasks(user_id=user_id)
        return tasks[task_id - 1]["task_id"]
