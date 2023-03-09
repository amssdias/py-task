import unittest
from unittest.mock import MagicMock, Mock, patch

from apps.accounts.controller import AccountsController
from apps.accounts.model import Users
from apps.accounts.view import AccountsView


class TestAccountsController(unittest.TestCase):

    def setUp(self) -> None:
        self.controller = AccountsController()
        self.controller.model.database = MagicMock()
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
        register_info = ("test@testing.com", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.model.create_user = Mock()
        self.controller.view.info = Mock()

        mock = Mock()
        result = self.controller.register(mock)

        self.assertTrue(result)

    def test_register_ask_register_called(self):
    
        register_info = ("test@testing.com", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.model.create_user = Mock()
        self.controller.view.info = Mock()

        mock = Mock()
        self.controller.register(mock)

        self.controller.view.ask_register.assert_called_once()

    def test_register_create_user_called(self):
        register_info = ("test@testing.com", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.model.create_user = Mock()
        self.controller.view.info = Mock()

        mock = Mock()
        self.controller.register(mock)

        self.controller.model.create_user.assert_called_once()
        self.controller.model.create_user.assert_called_once_with("test@testing.com", "12345678")

    def test_register_info_called(self):
        register_info = ("test@testing.com", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.model.create_user = Mock()
        self.controller.view.info = Mock()

        mock = Mock()
        self.controller.register(mock)

        self.controller.view.info.assert_called_once()
        self.controller.view.info.assert_called_once_with("User registered successfully")

    def test_register_invalid_email(self):
        register_info = ("test", "12345678", "12345678")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.view.error = Mock()
        mock = Mock()
        result = self.controller.register(mock)

        self.assertFalse(result)

        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Email not valid.")

    def test_register_invalid_password_length(self):
        register_info = ("test@testing.com", "1234567", "1234567")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.view.error = Mock()
        mock = Mock()
        result = self.controller.register(mock)

        self.assertFalse(result)

        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Password too short.")

    def test_register_invalid_password_mismatch(self):
        register_info = ("test@testing.com", "12345678", "12345679")
        self.controller.view.ask_register = Mock(return_value=register_info)
        self.controller.view.error = Mock()
        mock = Mock()
        result = self.controller.register(mock)

        self.assertFalse(result)

        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Passwords mismatch!")

    def test_logout(self):
        self.controller.view.info = Mock()
        c = Mock()
        self.controller.logout(c)

        self.assertEqual(False, c.user_logged)

    def test_logout_view_info_called(self):
        self.controller.view.info = Mock()
        c = Mock()
        self.controller.logout(c)

        self.controller.view.info.assert_called_once()
        self.controller.view.info.assert_called_once_with("User logged out.")

    def test_reset_password(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=True)
        self.controller.view.ask_user_password = Mock(side_effect=["12345678", "12345678"])
        self.controller.validate_password = Mock(return_value=True)
        self.controller.view.info = Mock()

        c = Mock()
        result = self.controller.reset_password(c)

        self.assertTrue(result)

    def test_reset_password_unexisted_user(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=False)
        self.controller.view.error = Mock()

        c = Mock()
        result = self.controller.reset_password(c)

        self.assertFalse(result)
        self.controller.model.get_user.assert_called_once()
        self.controller.model.get_user.assert_called_once_with("test@testing.com")
        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Sorry, user does not exist. Register first.")

    def test_reset_password_mismatch_passwords(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=True)
        self.controller.view.ask_user_password = Mock(side_effect=["12345678", "12345679"])
        self.controller.view.error = Mock()

        c = Mock()
        result = self.controller.reset_password(c)

        self.assertFalse(result)
        self.controller.view.ask_user_password.assert_called()
        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Passwords mismatch!")

    def test_reset_password_short_length(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=True)
        self.controller.view.ask_user_password = Mock(side_effect=["1234567", "1234567"])
        self.controller.view.error = Mock()

        c = Mock()
        result = self.controller.reset_password(c)

        self.assertFalse(result)
        self.controller.view.ask_user_password.assert_called()
        self.controller.view.error.assert_called_once()
        self.controller.view.error.assert_called_once_with("Password too short.")

    def test_reset_password_validate_password_called(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=True)
        self.controller.view.ask_user_password = Mock(side_effect=["12345678", "12345678"])
        self.controller.validate_password = Mock(return_value=False)
        self.controller.view.error = Mock()

        c = Mock()
        result = self.controller.reset_password(c)

        self.assertFalse(result)
        self.controller.validate_password.assert_called_once()
        self.controller.validate_password.assert_called_once_with("12345678", "12345678")

    def test_reset_password_database_updated(self):
        self.controller.view.ask_user_email = Mock(return_value="test@testing.com")
        self.controller.model.get_user = Mock(return_value=True)
        self.controller.view.ask_user_password = Mock(side_effect=["12345678", "12345678"])
        self.controller.validate_password = Mock(return_value=True)
        self.controller.model.update = Mock()
        self.controller.view.info = Mock()

        c = Mock()
        self.controller.reset_password(c)

        self.controller.model.update.assert_called_once()
        self.controller.model.update.assert_called_once_with(email="test@testing.com", new_values={"password": "12345678"})
        self.controller.view.info.assert_called_once()

    def test_validate_register_inputs(self):
        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="12345678",
            password_="12345678"
        )

        self.assertTrue(result)

    def test_validate_register_inputs_invalid_email(self):
        self.controller.view.error = Mock()

        result = self.controller.validate_register_inputs(
            email="test@",
            password="12345678",
            password_="12345678"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_invalid_password_length(self):
        self.controller.view.error = Mock()

        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="1234567",
            password_="1234567"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_invalid_password_mismatch(self):
        self.controller.view.error = Mock()

        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="12345678",
            password_="12345679"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_validations_called(self):
        self.controller.validate_email = Mock(return_value=True)
        self.controller.validate_password = Mock(return_value=True)

        self.controller.validate_register_inputs(
            email="test@testing.com",
            password="12345678",
            password_="12345679"
        )

        self.controller.validate_email.assert_called_once()
        self.controller.validate_password.assert_called_once()

    def _test_validate_email(self):
        pass

    def _test_validate_password(self):
        pass
