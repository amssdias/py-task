from apps.accounts.controller import AccountsController
from .controller import TodoController


accounts_controller = AccountsController()


TODO_MENU = """
1 - View my Tasks
2 - Create new Task
3 - Update Task
4 - Delete Task
5 - Logout
0 - Exit
"""

TODO_MENU_ACTIONS = {
    1: "View my tasks",
    2: "Create new task",
    3: "Update task",
    4: "Delete Task",
    5: accounts_controller.logout,
    0: "Exit",
}
