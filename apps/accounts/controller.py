import re
from typing import Optional, Dict
from apps.accounts.constants.database import ACTIVE

from apps.accounts.model import Users
from apps.accounts.utils.password import Password
from apps.accounts.utils.send_pin_email import send_account_activation_pin_email
from apps.accounts.view import AccountsView

from settings.database import redis_connection


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
        elif not user["active"]:
            self.view.error("It seems like your account is not active. Check your email for a pin we sent to you, so you can activate it.")
            pin = self.view.ask_pin()
            
            if not self.validate_pin(pin=pin, email=email):
                return False
        
        password_is_valid = Password.check_password(password, user["password"])

        if password_is_valid:
            controller.user_logged = True
            controller.user_email = email
            controller.user_id = user["user_id"]
            self.view.info("User logged successfully.")
            return True
        
        self.view.error("Password incorrect.")
        return False

    def register(self, _) -> bool:
        email, password, password_ = self.view.ask_register()

        user_cleaned_data = self.validate_register_inputs(email, password, password_)
        
        if not user_cleaned_data:
            return False

        user_created = self.model.create_user(email, password)
        if user_created:
            # TODO: Send email async
            send_account_activation_pin_email(email)

            self.view.info("User registered successfully, check your email to activate your account.")
        else:
            self.view.error("Sorry something went wrong. Try again.")

        return True

    def logout(self, controller) -> None:
        controller.user_logged = False
        controller.user_email = None
        controller.user_id = None
        self.view.info("User logged out.")

    def reset_password(self, _) -> bool:
        email = self.view.ask_user_email()

        if not self.model.get_user(email):
            self.view.error("Sorry, user does not exist. Register first.")
            return False

        send_account_activation_pin_email(email)
        
        pin = self.view.ask_pin()
        if not self.validate_pin(pin=pin, email=email):
            self.view.error("Sorry pin is not correct, check your email again.")

        password = self.view.ask_user_password(prompt="Enter your new password: ")
        password_ = self.view.ask_user_password(prompt="Enter your new password again: ")

        if not self.validate_password(password, password_):
            return False

        if not self.model.update(email=email, new_values={"password": password}):
            self.view.error("Sorry we had problems with the database, try again later.")
            return False
        
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

    def validate_pin(self, pin: str, email: str) -> bool:
        user_pin = redis_connection.get(email)
        
        if not user_pin:
            self.view.info("Looks like your pin was expired, we will send you a new one right now!")
            self.view.info("Check you email inbox. And try to login again.")

            send_account_activation_pin_email(email)

            return False
        
        elif user_pin.decode("utf-8") == pin:
            try:
                self.model.update(email=email, new_values={ACTIVE: 1})
                self.view.info("Your account is now active.")
                return True
            except Exception as e:
                # TODO: Logs
                self.view.error("Sorry something went wrong. Contact with admin.")
                return False
