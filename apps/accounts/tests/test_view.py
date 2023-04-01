import unittest
from unittest.mock import Mock, patch

from colorama import Fore

from apps.accounts.view import AccountsView


class TestAccountsView(unittest.TestCase):

    def setUp(self) -> None:
        self.view = AccountsView()
        return super().setUp()
    
    @patch("builtins.input", return_value="testing")
    def test_ask_user_email_return_value(self, mocked_input):
        result = self.view.ask_user_email()
        self.assertEqual("testing", result)
        self.assertIsInstance(result, str)

    @patch("builtins.input")
    def test_ask_user_email_input_called(self, mocked_input):
        self.view.ask_user_email()
        mocked_input.assert_called_once()
        mocked_input.assert_called_with(Fore.GREEN + "Enter your email: ")

    @patch("apps.accounts.view.getpass", return_value="12345678")
    def test_ask_user_password_return_value(self, mocked_input):
        result = self.view.ask_user_password()
        self.assertEqual("12345678", result)
        self.assertIsInstance(result, str)

    @patch("apps.accounts.view.getpass", return_value="12345678")
    def test_ask_user_password_getpass_called(self, mocked_getpass):
        self.view.ask_user_password()
        mocked_getpass.assert_called_once()
        mocked_getpass.assert_called_with(Fore.GREEN + "Enter your password: ")

    def test_ask_login_result_value(self):
        name = "testing_name"
        password = "12345678"
        self.view.ask_user_email = Mock(return_value=name)
        self.view.ask_user_password = Mock(return_value=password)
        result = self.view.ask_login()

        self.assertEqual((name, password), result)
        self.assertIsInstance(result, tuple)

    def test_ask_login_methods_called(self):
        self.view.ask_user_email = Mock()
        self.view.ask_user_password = Mock()
        self.view.ask_login()

        self.view.ask_user_email.assert_called_once()
        self.view.ask_user_password.assert_called_once()

    def test_ask_register_return_value(self):
        name = "testing_name"
        password = "12345678"
        self.view.ask_user_email = Mock(return_value=name)
        self.view.ask_user_password = Mock(return_value=password)
        result = self.view.ask_register()

        self.assertEqual((name, password, password), result)
        self.assertIsInstance(result, tuple)

    def test_ask_register_methods_called(self):
        self.view.ask_user_email = Mock()
        self.view.ask_user_password = Mock()
        self.view.ask_register()

        self.view.ask_user_email.assert_called_once()
        self.view.ask_user_password.assert_called()
        self.assertEqual(2, self.view.ask_user_password.call_count)

    @patch("builtins.print")
    def test_info_return_value(self, mocked_print):
        result = self.view.info("Hey")
        self.assertIsNone(result)

    @patch("builtins.print")
    def test_info_print_called(self, mocked_print):
        self.view.info("Hey")
        mocked_print.assert_called_once()
        mocked_print.assert_called_once_with(Fore.CYAN + "Hey")

    @patch("builtins.print")
    def test_error_return_value(self, mocked_print):
        result = self.view.error()
        self.assertIsNone(result)

    @patch("builtins.print")
    def test_info_print_called(self, mocked_print):
        self.view.error("error")
        mocked_print.assert_called_once()
        mocked_print.assert_called_once_with(Fore.RED + "error")
