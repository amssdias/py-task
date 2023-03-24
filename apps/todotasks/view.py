from colorama import Fore


class TodoView:

    def prompt_user_question(self, question):
        return input(Fore.GREEN + question)
    
    def info(self, prompt) -> None:
        print(Fore.CYAN + prompt)

    def error(self, prompt="Something went bad") -> None:
        print(Fore.RED + prompt)

    def display_list_tasks(self, tasks) -> None:
        if not tasks:
            self.info("There are no tasks yet, create a few first.")
            return None

        for index, task in enumerate(tasks):
            print(Fore.CYAN + f"{index + 1}: {task}")
