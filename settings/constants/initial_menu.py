from apps.accounts.controller import AccountsController


accounts_controller = AccountsController()


INITIAL_MENU = {
    1: accounts_controller.login,
    2: accounts_controller.register,
}
