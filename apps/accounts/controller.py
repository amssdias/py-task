import re
from typing import Optional, Dict

from apps.accounts.model import Users
from apps.accounts.utils.password import Password
from apps.accounts.view import AccountsView


class AccountsController:

    def __init__(self):
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
        
        self.view.error("Password incorrect.")
        return False

    def register(self, _) -> bool:
        email, password, password_ = self.view.ask_register()

        user_cleaned_data = self.validate_register_inputs(email, password, password_)
        
        if not user_cleaned_data:
            return False

        self.model.create_user(email, password)
        self.view.info("User registered successfully")
        return True

    def logout(self, controller) -> None:
        controller.user_logged = False
        self.view.info("User logged out.")

    def reset_password(self, _) -> bool:
        email = self.view.ask_user_email()

        if not self.model.get_user(email):
            self.view.error("Sorry, user does not exist. Register first.")
            return False

        # TODO:
        # - Create a pin
        # - Send an email with that pin
        # - Ask user to enter that pin here so we confirm it's him
        # - Ask him to prompt his new password and update

        password = self.view.ask_user_password(prompt="Enter your new password: ")
        password_ = self.view.ask_user_password(prompt="Enter your new password again: ")

        if not self.validate_password(password, password_):
            return False
        
        self.model.update(email=email, new_values={"password": password})
        self.view.info("Password updated.")
        return True

    def validate_register_inputs(self, email: str, password: str, password_: str) -> Optional[Dict]:
        email = self.validate_email(email)
        password = self.validate_password(password, password_)

        if not email or not password:
            return None
        
        return {"email": email, "password": password}


    def validate_email(self, email: str) -> str:
        if not isinstance(email, str):
            raise TypeError(f"Input {email} must be a str.")

        email = email.strip()
        email_regex = re.compile(r"@[a-zA-Z-\d]+\.(com|net|es|org)$")
        if not email_regex.search(email) or self.model.get_user(email):
            self.view.error("Email not valid.")
            return None

        return email

    def validate_password(self, password: str, password_: str) -> str:
        if password != password_ or len(password) < 8:
            self.view.error(
                "Password too short." if len(password) < 8 else "Passwords mismatch!" 
            )
            return None

        return password
