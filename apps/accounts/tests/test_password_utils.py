import hashlib
import unittest
from unittest.mock import patch

from apps.accounts.utils.password import Password
from settings.settings import SECRET_KEY


class TestPassword(unittest.TestCase):

    def setUp(self) -> None:
        self.password = Password()
        self.test_password = "qwerty1234"
        return super().setUp()
    
    def test_hash_password(self):
        result = self.password.hash_password(self.test_password)
        self.assertIsInstance(result, str)

    def test_hash_password_calls_salt_password(self):
        with patch("apps.accounts.utils.password.Password.salt_password") as mocked_salt_password:
            with patch("apps.accounts.utils.password.Password.get_hashed_password"):
                mocked_salt_password.return_value = self.test_password
                self.password.hash_password(self.test_password)

                mocked_salt_password.assert_called_once()
                mocked_salt_password.assert_called_once_with(self.test_password)

    def test_hash_password_calls_get_hashed_password(self):
        with patch("apps.accounts.utils.password.Password.salt_password"):
            with patch("apps.accounts.utils.password.Password.get_hashed_password") as mocked_get_hashed_password:
                self.password.hash_password(self.test_password)
                salted_password = self.password.salt_password(self.test_password)

                mocked_get_hashed_password.assert_called_once()
                mocked_get_hashed_password.assert_called_once_with(salted_password)

    def test_salt_password(self):
        result = self.password.salt_password(self.test_password)
        expected = str(self.test_password + SECRET_KEY).encode(self.password.encode_format)

        self.assertEqual(expected, result)
        self.assertIsInstance(result, bytes)

    def test_get_hashed_password(self):
        password = bytes(self.test_password.encode(self.password.encode_format))
        result = self.password.get_hashed_password(password)

        hash_object = hashlib.sha256()
        hash_object.update(password)
        expected = hash_object.hexdigest()

        self.assertEqual(expected, result)
        self.assertIsInstance(result, str)

    def test_check_password(self):
        hashed_password = self.password.hash_password(self.test_password)
        result = self.password.check_password(password=self.test_password, hashed_password=hashed_password)

        self.assertTrue(result)
