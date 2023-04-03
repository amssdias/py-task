from typing import Union
from apps.todotasks.model import TodoModel
from apps.todotasks.view import TodoView


class TodoController:

    def __init__(self):
        self.model = TodoModel()
        self.view = TodoView()
    
    def create_new_task(self, controller) -> bool:
        new_task = self.view.prompt_user_question("Type new task: ")
        task = self.model.create_task(user_id=controller.user_id, new_task=new_task)
        if task:
            self.view.info("Task created successfully.")
            return True
        self.view.error("Task was not saved. Something went wrong. Try again.")
        return False

    def display_all_tasks(self, controller) -> bool:
        tasks = self.model.get_all_tasks(user_id=controller.user_id)
        if tasks:
            self.view.display_list_tasks(tasks)
            return True
        return False

    def update_task(self, controller) -> bool:
        task_id = self.get_and_validate_task_id(user_id=controller.user_id)
        if not task_id:
            return False
        new_task = input("New task name: ").strip()
        real_task_id = self.model.get_task_id(user_id=controller.user_id, task_id=task_id)
        self.model.update(user_id=controller.user_id, task_id=real_task_id, new_task=new_task)
        self.view.info("Task updated!")
        return True

    def delete_task(self, controller) -> bool:
        task_id = self.get_and_validate_task_id(user_id=controller.user_id)
        if not task_id:
            return False
        real_task_id = self.model.get_task_id(user_id=controller.user_id, task_id=task_id)
        self.model.delete(user_id=controller.user_id, task_id=real_task_id)
        self.view.info(f"Task with id '{task_id}' deleted.")
        return True

    def get_and_validate_task_id(self, user_id) -> Union[bool, int]:
        tasks = self.model.get_all_tasks(user_id=user_id)
        if not tasks:
            self.view.error("You don't have any tasks.")
            return False
        try:
            task_id = int(input("Task id: "))
            if task_id > len(tasks) or task_id < 0:
                raise Exception
        except ValueError as e:
            self.view.error("Task id must be a number")
            return False
        except Exception as e:
            self.view.error(f"We couldn't find a task with the id of '{task_id}'")
            return False

        return task_id