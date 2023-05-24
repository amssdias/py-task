from typing import Dict, List
from colorama import Fore


class TodoView:

    def prompt_user_question(self, question) -> str:
        return input(Fore.GREEN + question)
    
    def info(self, prompt) -> None:
        print(Fore.CYAN + prompt)

    def error(self, prompt="Something went bad") -> None:
        print(Fore.RED + prompt)

    def display_list_tasks(self, tasks: List[Dict]) -> None:
        fields = {
            "task_description": "Description",
            "status": "Status",
            "priority": "Priority",
            "due_date": "Due date",
            "created_at": "Created",
        }

        no_display_fields = ["task_id", "task_name", "user_id"]

        if not tasks:
            self.info("There are no tasks yet, create a few first.")
            return None

        for index, task in enumerate(tasks):
            print(Fore.RESET + task['task_name'])
            print(Fore.CYAN + f"ID: {index + 1}")

            for field in no_display_fields:
                task.pop(field)

            for key, value in task.items():
                if value:
                    print(Fore.CYAN + f"{fields[key]}: " + Fore.RESET + value)
                else:
                    print(Fore.CYAN + f"{fields[key]}: " + Fore.RESET + "----")
            print()
