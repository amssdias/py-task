import os
import unittest
from unittest.mock import patch

from apps.accounts.model import Users
from apps.accounts.utils.password import Password
from settings.database.utils import create_tables_database
from settings.tests.database import TestDatabaseConnection


class TestUsersModel(unittest.TestCase):
    
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        with self.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users")
        return super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = Users()
        cls.model.database = TestDatabaseConnection
        create_tables_database(cls.model.database.database_path)
        cls.user_email = "test@testing.com"
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.model.database.database_path):
            os.remove(cls.model.database.database_path)
        return super().tearDownClass()

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
        with self.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            user = dict(cursor.fetchone())

        self.assertEqual(user["email"], self.user_email)

    def test_update_user(self):
        self.model.create_user(self.user_email, "password1234")
        new_password = "new-password1234"
        user_updated = self.model.update(self.user_email, {"password": new_password})

        hashed_password = Password.hash_password(new_password)
        self.assertTrue(user_updated)

        with self.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ?", (self.user_email,))
            user = dict(cursor.fetchone())

        self.assertEqual(user["password"], hashed_password)

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
