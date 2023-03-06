import sys
from typing import Optional
from apps.accounts.constants import ACCOUNTS_MENU, ACCOUNTS_MENU_ACTIONS
from apps.todotasks.constants import TODO_MENU, TODO_MENU_ACTIONS



class MainController:

    def __init__(self):
        self._user_logged = False
        self.menu_actions = ACCOUNTS_MENU_ACTIONS

    @property
    def user_logged(self):
        return self._user_logged

    @user_logged.setter
    def user_logged(self, value):
        self._user_logged = value
        if value:
            self.menu_actions = TODO_MENU_ACTIONS
        else:
            self.menu_actions = ACCOUNTS_MENU_ACTIONS

    def start_app(self):
        print("Starting app...")

        while True:
            user_option = self.get_menu_option()
            if user_option == 0:
                print("Goodbye.")
                sys.exit()

            user_choice = self.menu_actions.get(user_option, None)
            if not user_choice:
                print("Choose only one of the options on the menu.")
                continue
            
            user_choice(self)

    def get_menu_option(self) -> Optional[int]:
        if self.user_logged:
            user_option = input(TODO_MENU)
        else:
            user_option = input(ACCOUNTS_MENU)
        return self.validate_user_option(user_option)

    def validate_user_option(self, user_option: str) -> Optional[int]:
        if not user_option.isdigit() or not self.menu_actions.get(int(user_option), None):
            print("Sorry, option not available")
            return None
        return int(user_option)
