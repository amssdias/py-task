import os
import unittest

from apps.todotasks.model import TodoModel
from settings.database.utils import create_tables_database, dict_factory
from settings.tests.database import TestDatabaseConnection


class TestTodoModel(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        with self.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks")
        return super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = TodoModel()
        cls.model.database = TestDatabaseConnection
        create_tables_database(cls.model.database.database_path)

        email = "test@fake.com"
        with cls.model.database(TestDatabaseConnection) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users(email, password) VALUES(?, ?)", (email, "12345678"))
            cls.user = cursor.execute("SELECT user_id, email, password, created_at FROM users WHERE email = ?", (email,)).fetchone()

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.model.database.database_path):
            os.remove(cls.model.database.database_path)
        return super().tearDownClass()

    def test_create_task(self):
        new_task = "New task"
        result = self.model.create_task(self.user["user_id"], new_task)

        self.assertTrue(result)

    def test_create_task_created(self):
        new_task = "New task"
        self.model.create_task(self.user["user_id"], new_task)

        with self.model.database(TestDatabaseConnection) as connection:
            cursor = connection.cursor()
            task = cursor.execute("SELECT task_name FROM tasks WHERE user_id = ?", (self.user["user_id"],)).fetchone()
        
        task = dict(task)
        self.assertEqual(task["task_name"], new_task)

    def test_update_task(self):
        new_task = "New task"
        self.model.create_task(self.user["user_id"], new_task)

        with self.model.database(TestDatabaseConnection) as connection:
            cursor = connection.cursor()
            task = cursor.execute("SELECT task_id, task_name FROM tasks WHERE user_id = ?", (self.user["user_id"],)).fetchone()
        
        task = dict(task)
        result = self.model.update(self.user["user_id"], task["task_id"], "Task updated")

        self.assertTrue(result)

    def test_update_task_wrong_task_id(self):
        result = self.model.update(self.user["user_id"], 10000, "Task updated")

        self.assertFalse(result)

    def test_get_all_tasks(self):
        self.model.create_task(self.user["user_id"], "New task")
        result = self.model.get_all_tasks(self.user["user_id"])

        self.assertIsInstance(result, list)

    def test_get_all_tasks_no_tasks(self):
        result = self.model.get_all_tasks(self.user["user_id"])

        self.assertEqual(None, result)

    def test_delete_task(self):
        self.model.create_task(self.user["user_id"], "New task")
        with self.model.database(TestDatabaseConnection) as connection:
            cursor = connection.cursor()
            task = cursor.execute("SELECT task_id, task_name FROM tasks WHERE user_id = ?", (self.user["user_id"],)).fetchone()
        
        task = dict(task)

        result = self.model.delete(self.user["user_id"], task["task_id"])

        self.assertTrue(result)

    def test_delete_task_no_task(self):
        result = self.model.delete(self.user["user_id"], 10000)

        self.assertFalse(result)

    def test_get_task_id(self):
        self.model.create_task(self.user["user_id"], "New task")

        with self.model.database(TestDatabaseConnection) as connection:
            cursor = connection.cursor()
            task = cursor.execute("SELECT task_id, task_name FROM tasks WHERE user_id = ?", (self.user["user_id"],)).fetchone()
        task = dict(task)
        
        result = self.model.get_task_id(self.user["user_id"], 1)
        self.assertEqual(task["task_id"], result)
