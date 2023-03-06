from apps.accounts.model import Users
from apps.accounts.utils.password import Password
from apps.accounts.view import AccountsView


class AccountsController:

    def __init__(self):
        self.user = None
        self.model = Users()
        self.view = AccountsView()

    def login(self, controller) -> bool:
        email, password = self.view.ask_login()
        user = self.model.get_user(email)

        if not user:
            self.view.error("User not registered.")
            return False
        
        password_is_valid = Password.check_password(password, user["password"])

        if password_is_valid:
            controller.user_logged = True
            self.view.info("User logged successfully.")
        return True

    def register(self, _) -> False:
        email, password, password_ = self.view.ask_register()

        if not self.validate_email(email):
            self.view.error("Email not valid.")
            return False 
        elif not self.validate_password(password, password_):
            self.view.error("Sorry, passwords didn't match.")
            return False 

        self.model.create_user(email, password)
        self.view.info("User registered successfully")
        return True

    def logout(self, controller):
        controller.user_logged = False
        self.view.info("User logged out.")

    def validate_email(self, email: str) -> bool:
        return True

    def validate_password(self, password: str, password_: str) -> bool:
        return True
