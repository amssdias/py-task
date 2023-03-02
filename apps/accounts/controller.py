from getpass import getpass
from apps.accounts.model import Users
from apps.accounts.utils.password import Password


class AccountsController:

    def __init__(self):
        self.user = None
        self.model = Users()

    def login(self, controller) -> bool:
        email = input("Enter your email: ")
        password = getpass("Enter your email: ")
        user = self.model.get_user(email)

        if not user:
            print("User not registered.")
            return False
        
        password_is_valid = Password.check_password(password, user["password"])

        if password_is_valid:
            controller.user_logged = True
        return True

    def register(self, _) -> False:
        # Get user email
        email = input("Enter your email: ")

        # Get 2 passwords
        password = getpass("Enter your password: ")
        password_ = getpass("Enter your password again: ")

        # Validate
        if not self.validate_email(email):
            print("Sorry, email is not valid.")
            return False 
        elif not self.validate_password(password, password_):
            print("Sorry, passwords didn't match.")
            return False 

        self.model.create_user(email, password)
        return True

    def logout(self, email):
        pass

    def validate_email(self, email: str) -> bool:
        return True

    def validate_password(self, password: str, password_: str) -> bool:
        return True
