import os
import unittest
from unittest.mock import Mock, patch

from apps.todotasks.controller import TodoController
from apps.todotasks.model import TodoModel
from settings.database.utils import create_tables_database
from settings.tests.database import TestDatabaseConnection


class TestTodoController(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.controller = TodoController()
        cls.controller.model = TodoModel(database_path=TestDatabaseConnection.database_path)
        create_tables_database(cls.controller.model.database_path)
        cls.main_controller = Mock()
        cls.main_controller.user_id = 1
        cls.main_controller.user_email = "test@testing.com"
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.controller.model.database_path):
            os.remove(cls.controller.model.database_path)
        return super().tearDownClass()
    
    def test_create_new_task(self):
        self.controller.view.prompt_user_question = Mock(return_value="New task")
        self.controller.model.create_task = Mock(return_value=True) 
        self.controller.view.info = Mock()
        result = self.controller.create_new_task(self.main_controller)

        self.assertTrue(result)
        self.controller.view.prompt_user_question.assert_called_once_with("Type new task: ")
        self.controller.model.create_task.assert_called_once()
        self.controller.view.info.assert_called_once_with("Task created successfully.")

    def test_create_new_task_nonexisting_user(self):
        self.controller.view.prompt_user_question = Mock(return_value="New task")
        self.controller.model.create_task = Mock(return_value=False) 
        self.controller.view.error = Mock()
        result = self.controller.create_new_task(self.main_controller)

        self.assertFalse(result)
        self.controller.view.prompt_user_question.assert_called_once()
        self.controller.view.error.assert_called_once_with("Task was not saved. Something went wrong. Try again.")

    def _test_create_new_task_created(self):
        # TODO: Review why it's using main database to insert and get values
        self.controller.view.prompt_user_question = Mock(return_value="New task")
        self.controller.view.info = Mock()
        self.controller.create_new_task(self.main_controller)

        with self.controller.model.database() as connection:
            cursor = connection.cursor()
            task = cursor.execute("SELECT * FROM tasks").fetchall()

        self.assertTrue(task)
        # self.assertEqual("New task", task)

    @patch("apps.todotasks.view.print")
    def _test_display_all_tasks(self, mocked_print):
        # TODO: Review why it's using main database to insert and get values
        with self.controller.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tasks(task_name, user_id) VALUES('first task', 1)")

        with self.controller.model.database() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks")
            c = cursor.fetchall()

            for cc in c:
                print(dict(cc))

        result = self.controller.display_all_tasks(self.main_controller)
        # self.assertTrue(result)

    @patch("builtins.print")
    def test_display_all_tasks_func_called(self, mocked_print):
        self.controller.model.get_all_tasks = Mock()
        self.controller.view.display_list_tasks = Mock()
        self.controller.display_all_tasks(self.main_controller)

        self.controller.model.get_all_tasks.assert_called_once_with(user_id=self.main_controller.user_id)
        self.controller.view.display_list_tasks.assert_called_once()

    def _test_update_task(self):
        self.controller.get_and_validate_task_id = Mock(return_value=1)

        result = self.controller.update_task(self.main_controller)

    def test_delete_task(self):
        pass

    def test_get_and_validate_task_id(self):
        pass
