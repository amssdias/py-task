from typing import List, Optional
from settings.database import db_instance as database

class TodoModel:

    def __init__(self):
        self.database = database
    
    def create_task(self, user_email: str, new_task: str) -> bool:
        for user in self.database["users"]:
            if user["email"] == user_email:
                task = user.setdefault("tasks", [new_task])
                if new_task not in task:
                    user["tasks"].extend([new_task])
                return True
        return False

    def update(self, user_email, task_id, new_task):
        for user in self.database["users"]:
            if user["email"] == user_email:
                user["tasks"][task_id - 1] = new_task
                return True
        return False

    def get_all_tasks(self, user_email) -> Optional[List]:
        for user in self.database["users"]:
            if user["email"] == user_email:
                return user.get("tasks")
        return False
    
    def delete(self, user_email, task_id) -> bool:
        for user in self.database["users"]:
            if user["email"] == user_email:
                user["tasks"].pop(task_id - 1)
                return True
        return False
