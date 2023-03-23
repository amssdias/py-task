import unittest
from unittest.mock import patch

from apps.accounts.model import Users
from apps.accounts.utils.password import Password
from settings.database import db_instance as database


class TestUsersModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Users()
        self.model.database.clear()
        self.user_email = "test@testing.com"
        return super().setUp()
    
    def test_create_user(self):
        user_created = self.model.create_user(self.user_email, "password1234")
        self.assertTrue(user_created)

    @patch("apps.accounts.model.Password.hash_password", return_value="pass1234")
    def test_create_user_hash_password_called(self, mocked_hash_password):
        self.model.create_user(self.user_email, "password1234")

        mocked_hash_password.assert_called_once()
        mocked_hash_password.assert_called_once_with("password1234")

    def test_create_user_created(self):
        self.model.create_user(self.user_email, "password1234")
        self.assertTrue(database["users"])

    def test_update_user(self):
        self.model.create_user(self.user_email, "password1234")
        new_password = "new-password1234"
        user_updated = self.model.update(self.user_email, {"password": new_password})

        hashed_password = Password.hash_password(new_password)
        self.assertTrue(user_updated)
        self.assertEqual(database["users"][0]["password"], hashed_password)

    def test_update_user_nonexisting_user(self):
        user_updated = self.model.update(self.user_email, {"password": "new-password1234"})
        self.assertFalse(user_updated)

    @patch("apps.accounts.model.Password.hash_password", return_value="new-password")
    def test_update_user_hash_password_called(self, mocked_hash_password):
        self.model.create_user(self.user_email, "password1234")
        self.model.update(self.user_email, {"password": "new_password"})
        mocked_hash_password.assert_called_with("new_password")

    def test_get_user(self):
        self.model.create_user(self.user_email, "password1234")
        result = self.model.get_user(self.user_email)

        self.assertEqual(self.user_email, result["email"])

    def test_get_user_nonexisting(self):
        result = self.model.get_user(self.user_email)

        self.assertIsNone(result)

    