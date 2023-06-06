import unittest
from unittest.mock import MagicMock, Mock, patch

from apps.accounts.controller import AccountsController
from apps.accounts.model import Users
from apps.accounts.view import AccountsView


class TestAccountsController(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.controller = AccountsController()
        cls.controller.model.database = MagicMock()
        return super().setUpClass()

    def setUp(self) -> None:
        self.controller.view.info = Mock()
        self.controller.view.error = Mock()
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

        with patch.object(self.controller.view, "ask_login", return_value=(email, password)), \
            patch.object(self.controller.model, "get_user", return_value={"user_id": 1, "password": password, "active": 1}), \
            patch("apps.accounts.utils.password.Password.check_password") as mocked_check_password:
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

        with patch.object(self.controller.view, "ask_login", return_value=(email, password)), \
            patch.object(self.controller.model, "get_user", return_value=False):

            mock = Mock()
            result = self.controller.login(mock)

            self.assertFalse(result)

            self.controller.view.ask_login.assert_called_once()
            self.controller.model.get_user.assert_called_once()
            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("User not registered.")

    def test_login_user_not_active(self):
        email = "testing"
        password = "12345678"

        with patch.object(self.controller.view, "ask_login", return_value=(email, password)), \
            patch.object(self.controller.model, "get_user", return_value={"user_id": 1, "password": password, "active": 0}), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller, "validate_pin", return_value=False):

            mock = Mock()
            result = self.controller.login(mock)

            self.assertFalse(result)

            self.controller.view.ask_login.assert_called_once()
            self.controller.model.get_user.assert_called_once()
            self.controller.model.get_user.assert_called_once_with(email)
            self.controller.view.error.assert_called_once()
            self.controller.view.ask_pin.assert_called_once()
            self.controller.validate_pin.assert_called_once()

    def test_login_password_incorrect(self):
        email = "testing"
        password = "12345678"

        with patch.object(self.controller.view, "ask_login", return_value=(email, password)), \
            patch.object(self.controller.model, "get_user", return_value={"password": password, "active": 1}), \
            patch("apps.accounts.utils.password.Password.check_password") as mocked_check_password:
            mocked_check_password.return_value = False

            mock = Mock()
            result = self.controller.login(mock)

            self.assertFalse(result)

            self.controller.view.ask_login.assert_called_once()
            self.controller.model.get_user.assert_called_once()
            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Password incorrect.")

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_register_successful(self, mocked_send_account_pin_email):
        register_info = ("test@testing.com", "12345678", "12345678")

        with patch.object(self.controller.view, "ask_register", return_value=register_info), \
            patch.object(self.controller.model, "create_user"):

            mock = Mock()
            result = self.controller.register(mock)

            self.assertTrue(result)
            mocked_send_account_pin_email.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_register_ask_register_called(self, mocked_send_account_pin_email):
        register_info = ("test@testing.com", "12345678", "12345678")

        with patch.object(self.controller.view, "ask_register", return_value=register_info), \
            patch.object(self.controller.model, "create_user"):

            mock = Mock()
            self.controller.register(mock)

            self.controller.view.ask_register.assert_called_once()
            mocked_send_account_pin_email.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_register_create_user_called(self, mocked_send_account_pin_email):
        register_info = ("test@testing.com", "12345678", "12345678")

        with patch.object(self.controller.view, "ask_register", return_value=register_info), \
            patch.object(self.controller.model, "create_user"):

            mock = Mock()
            self.controller.register(mock)

            self.controller.model.create_user.assert_called_once()
            self.controller.model.create_user.assert_called_once_with("test@testing.com", "12345678")
            mocked_send_account_pin_email.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_register_info_called(self, mocked_send_account_pin_email):
        register_info = ("test@testing.com", "12345678", "12345678")

        with patch.object(self.controller.view, "ask_register", return_value=register_info), \
            patch.object(self.controller.model, "create_user"):

            mock = Mock()
            self.controller.register(mock)

            self.controller.view.info.assert_called_once()
            self.controller.view.info.assert_called_once_with("User registered successfully, check your email to activate your account.")
            mocked_send_account_pin_email.assert_called_once()

    def test_register_invalid_email(self):
        register_info = ("test", "12345678", "12345678")

        with patch.object(self.controller.view, "ask_register", return_value=register_info):
            mock = Mock()
            result = self.controller.register(mock)

            self.assertFalse(result)

            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Email not valid.")

    def test_register_invalid_password_length(self):
        register_info = ("test@testing.com", "1234567", "1234567")

        with patch.object(self.controller.view, "ask_register", return_value=register_info):
            mock = Mock()
            result = self.controller.register(mock)

            self.assertFalse(result)

            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Password too short.")

    def test_register_invalid_password_mismatch(self):
        register_info = ("test@testing.com", "12345678", "12345679")

        with patch.object(self.controller.view, "ask_register", return_value=register_info):
            mock = Mock()
            result = self.controller.register(mock)

            self.assertFalse(result)

            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Passwords mismatch!")

    def test_logout(self):
        c = Mock()
        self.controller.logout(c)

        self.assertEqual(False, c.user_logged)

    def test_logout_view_info_called(self):
        c = Mock()
        self.controller.logout(c)

        self.controller.view.info.assert_called_once()
        self.controller.view.info.assert_called_once_with("User logged out.")

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_reset_password(self, mocked_send_account_pin_email):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller.view, "ask_user_password", side_effect=["12345678", "12345678"]), \
            patch.object(self.controller.model, "get_user", return_value=True), \
            patch.object(self.controller.model, "update", return_value=True), \
            patch.object(self.controller, "validate_pin", return_value=True), \
            patch.object(self.controller, "validate_password", return_value=True):

            c = Mock()
            result = self.controller.reset_password(c)

            self.assertTrue(result)
            mocked_send_account_pin_email.assert_called_once()

    def test_reset_password_unexisted_user(self):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.model, "get_user", return_value=False):

            c = Mock()
            result = self.controller.reset_password(c)

            self.assertFalse(result)
            self.controller.model.get_user.assert_called_once()
            self.controller.model.get_user.assert_called_once_with("test@testing.com")
            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Sorry, user does not exist. Register first.")

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_reset_password_mismatch_passwords(self, mocked_send_account_pin_email):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.view, "ask_user_password", side_effect=["12345678", "12345679"]), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller.model, "get_user", return_value=True), \
            patch.object(self.controller, "validate_pin", return_value=True):

            c = Mock()
            result = self.controller.reset_password(c)

            self.assertFalse(result)
            mocked_send_account_pin_email.assert_called_once()
            self.controller.view.ask_user_password.assert_called()
            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Passwords mismatch!")
            self.controller.view.ask_pin.assert_called_once()
            self.controller.validate_pin.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_reset_password_short_length(self, mocked_send_account_pin_email):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.view, "ask_user_password", side_effect=["1234567", "1234567"]), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller.model, "get_user", return_value=True), \
            patch.object(self.controller, "validate_pin", return_value=True):

            c = Mock()
            result = self.controller.reset_password(c)

            self.assertFalse(result)
            self.controller.view.ask_user_password.assert_called()
            self.controller.view.error.assert_called_once()
            self.controller.view.error.assert_called_once_with("Password too short.")
            self.controller.view.ask_pin.assert_called_once()
            self.controller.validate_pin.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_reset_password_validate_password_called(self, mocked_send_account_pin_email):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.view, "ask_user_password", side_effect=["12345678", "12345678"]), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller.model, "get_user", return_value=True), \
            patch.object(self.controller, "validate_pin", return_value=True), \
            patch.object(self.controller, "validate_password", return_value=False):

            c = Mock()
            result = self.controller.reset_password(c)

            self.assertFalse(result)
            self.controller.validate_password.assert_called_once()
            self.controller.validate_password.assert_called_once_with("12345678", "12345678")
            self.controller.view.ask_pin.assert_called_once()
            self.controller.validate_pin.assert_called_once()

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_reset_password_database_updated(self, mocked_send_account_pin_email):
        with patch.object(self.controller.view, "ask_user_email", return_value="test@testing.com"), \
            patch.object(self.controller.view, "ask_user_password", side_effect=["12345678", "12345678"]), \
            patch.object(self.controller.view, "ask_pin", return_value="1234"), \
            patch.object(self.controller.model, "get_user", return_value=True), \
            patch.object(self.controller.model, "update"), \
            patch.object(self.controller, "validate_pin", return_value=True), \
            patch.object(self.controller, "validate_password", return_value=True):

            c = Mock()
            self.controller.reset_password(c)

            self.controller.model.update.assert_called_once()
            self.controller.model.update.assert_called_once_with(email="test@testing.com", new_values={"password": "12345678"})
            self.controller.view.info.assert_called_once()
            self.controller.view.ask_pin.assert_called_once()
            self.controller.validate_pin.assert_called_once()

    def test_validate_register_inputs(self):
        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="12345678",
            password_="12345678"
        )

        self.assertTrue(result)

    def test_validate_register_inputs_invalid_email(self):
        result = self.controller.validate_register_inputs(
            email="test@",
            password="12345678",
            password_="12345678"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_invalid_password_length(self):
        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="1234567",
            password_="1234567"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_invalid_password_mismatch(self):
        result = self.controller.validate_register_inputs(
            email="test@testing.com",
            password="12345678",
            password_="12345679"
        )

        self.assertFalse(result)
        self.controller.view.error.assert_called_once()

    def test_validate_register_inputs_validations_called(self):
        with patch.object(self.controller, "validate_email", return_value=True), \
            patch.object(self.controller, "validate_password", return_value=True):

            self.controller.validate_register_inputs(
                email="test@testing.com",
                password="12345678",
                password_="12345679"
            )

            self.controller.validate_email.assert_called_once()
            self.controller.validate_password.assert_called_once()

    def test_validated_domain_emails(self):
        valid_domains = ["com", "net", "es", "org"]

        for domain in valid_domains:
            email = f"test@test.{domain}"
            validated_email = self.controller.validate_email(email)
            self.assertEqual(validated_email, email)
            self.assertIsInstance(validated_email, str)

    def test_validated_email_with_spaces(self):
        email = "   test@test.com   "
        validated_email = self.controller.validate_email(email)
        self.assertEqual(validated_email, email.strip())
        self.assertIsInstance(validated_email, str)

    def test_validate_email_wrong_types(self):
        not_allowed_types = [True, 123, 2.12, None]

        for type in not_allowed_types:
            with self.assertRaises(TypeError):
                self.controller.validate_email(type)

    @patch("builtins.print")
    def test_invalid_domain_email(self, mocked_print):
        email = "test@test.c"
        validated_email = self.controller.validate_email(email)
        self.assertEqual(validated_email, None)
        self.assertFalse(validated_email)

    def _test_validate_password(self):
        pass

    def test_validate_pin_successful(self):
        with patch.object(self.controller.model, "update"), \
            patch("apps.accounts.controller.redis_connection") as mocked_redis_connection:

            pin = "1234"
            mocked_redis_connection.get = Mock(return_value=pin.encode("utf-8"))

            result = self.controller.validate_pin(pin=pin, email="test@testing.com")

            self.assertTrue(result)
            mocked_redis_connection.get.assert_called_once_with("test@testing.com")
            self.controller.model.update.assert_called_once_with(email="test@testing.com", new_values={"active": 1})
            self.controller.view.info.assert_called_once_with("Your account is now active.")

    @patch("apps.accounts.controller.send_account_activation_pin_email")
    def test_validate_pin_expired(self, mocked_send_account_pin_email):
        with patch("apps.accounts.controller.redis_connection") as mocked_redis_connection:
            mocked_redis_connection.get = Mock(return_value=False)

            result = self.controller.validate_pin(pin="1234", email="test@testing.com")

        self.assertFalse(result)
        mocked_redis_connection.get.assert_called_once()
        self.controller.view.info.assert_called()
        mocked_send_account_pin_email.assert_called_once()
