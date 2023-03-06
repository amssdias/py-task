from apps.accounts.controller import AccountsController


accounts_controller = AccountsController()


ACCOUNTS_MENU = """
1 - Log in
2 - Register
0 - Exit
"""


ACCOUNTS_MENU_ACTIONS = {
    1: accounts_controller.login,
    2: accounts_controller.register,
}
