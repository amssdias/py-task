import colorama
from colorama import Fore

from getpass import getpass
from typing import Tuple


colorama.init(autoreset=True)


class AccountsView:

    def ask_user_email(self) -> str:
        return input(Fore.GREEN + "Enter your email: ")
    
    def ask_user_password(self, prompt="Enter your password: ") -> str:
        return getpass(Fore.GREEN + prompt)
    
    def ask_login(self) -> Tuple:
        return self.ask_user_email(), self.ask_user_password()
    
    def ask_register(self) -> Tuple:
        return self.ask_user_email(), self.ask_user_password(), self.ask_user_password(prompt="Enter your password again: ")

    def info(self, prompt) -> None:
        print(Fore.CYAN + prompt)

    def error(self, prompt="Something went bad") -> None:
        print(Fore.RED + prompt)