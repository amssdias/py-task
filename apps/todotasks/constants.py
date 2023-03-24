from apps.accounts.controller import AccountsController
from .controller import TodoController

accounts_controller = AccountsController()
todo_controller = TodoController()


TODO_MENU = """
1 - View my Tasks
2 - Create new Task
3 - Update Task
4 - Delete Task
5 - Logout
0 - Exit
"""

TODO_MENU_ACTIONS = {
    1: todo_controller.display_all_tasks,
    2: todo_controller.create_new_task,
    3: todo_controller.update_task,
    4: todo_controller.delete_task,
    5: accounts_controller.logout,
    0: "Exit",
}
