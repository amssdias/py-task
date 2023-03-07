import unittest
from unittest.mock import Mock, patch

from apps.accounts.controller import AccountsController
from apps.accounts.model import Users
from apps.accounts.view import AccountsView


class TestAccountsController(unittest.TestCase):

    def setUp(self) -> None:
        self.controller = AccountsController()
        return super().setUp()
    
    def test_initial_variables(self):
        instance_variables = self.controller.__dict__.keys()

        self.assertIn("model", instance_variables)
        self.assertIn("view", instance_variables)

    def test_initial_variables_values(self):
        self.assertIsInstance(self.controller.model, Users)
        self.assertIsInstance(self.controller.view, AccountsView)

    def test_login_successful(self):
        email = "testing"
        password = "12345678"
        self.controller.view.ask_login = Mock(return_value=(email, password))
        self.controller.view.info = Mock()
        self.controller.model.get_user = Mock(return_value={"password": password})

        with patch("apps.accounts.utils.password.Password.check_password") as mocked_check_password:
            mocked_check_password.return_value = True

            mock = Mock()
            result = self.controller.login(mock)

        self.assertTrue(result)

        self.controller.view.ask_login.assert_called_once()
        self.controller.model.get_user.assert_called_once()
        self.controller.model.get_user.assert_called_once_with(email)
        self.controller.view.info.assert_called_once()
        self.controller.view.info.assert_called_once_with("User logged successfully.")
        mocked_check_password.assert_called_once()

    def test_login_user_not_registered(self):
        email = "testing"
        password = "12345678"
        self.controller.view.ask_login = Mock(return_value=(email, password))
        self.controller.model.get_user = Mock(return_value=False)
        self.controller.view.error = Mock()

        mock = Mock()
        result = self.controller.login(mock)

        self.assertFalse(result)

        self.controller.view.ask_login.assert_called_once()
        self.controller.model.get_user.assert_called_once()
        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("User not registered.")

    def test_login_password_incorrect(self):
        email = "testing"
        password = "12345678"
        self.controller.view.ask_login = Mock(return_value=(email, password))
        self.controller.model.get_user = Mock(return_value={"password": password})
        self.controller.view.error = Mock()

        with patch("apps.accounts.utils.password.Password.check_password") as mocked_check_password:
            mocked_check_password.return_value = False

            mock = Mock()
            result = self.controller.login(mock)

        self.assertFalse(result)

        self.controller.view.ask_login.assert_called_once()
        self.controller.model.get_user.assert_called_once()
        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Password incorrect.")

    def test_register_successful(self):
        register_info = ("testing", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.model.create_user = Mock()
        self.controller.view.info = Mock()

        mock = Mock()
        result = self.controller.register(mock)

        self.assertTrue(result)

        self.controller.view.ask_register.assert_called_once()
        self.controller.model.create_user.assert_called_once()
        self.controller.view.info.assert_called_once()

    def _test_logout(self):
        pass

    def _test_reset_password(self):
        pass

    def _test_validate_email(self):
        pass

    def _test_validate_password(self):
        pass
