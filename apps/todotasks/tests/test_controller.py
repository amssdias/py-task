import os
import unittest
from unittest.mock import Mock, patch

from apps.todotasks.controller import TodoController
from apps.todotasks.model import TodoModel
from settings.database.utils import create_tables_database
from settings.tests.database import TestDatabaseConnection


class TestTodoController(unittest.TestCase):

    def setUp(self) -> None:
        self.controller.view.info = Mock()
        self.controller.view.error = Mock()
        return super().setUp()

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
        with patch.object(self.controller.model, "create_task", return_value=True) as mocked_create_task, \
            patch.object(self.controller.view, "prompt_user_question", return_value="New task"):

            result = self.controller.create_new_task(self.main_controller)

            self.assertTrue(result)
            self.controller.view.prompt_user_question.assert_called_once_with("Type new task: ")
            mocked_create_task.assert_called_once()
            self.controller.view.info.assert_called_once_with("Task created successfully.")

    def test_create_new_task_nonexisting_user(self):
        with patch.object(self.controller.model, "create_task", return_value=False) as mocked_create_task, \
            patch.object(self.controller.view, "prompt_user_question", return_value="New task"):

            result = self.controller.create_new_task(self.main_controller)

            self.assertFalse(result)
            self.controller.view.prompt_user_question.assert_called_once()
            mocked_create_task.assert_called_once()
            self.controller.view.error.assert_called_once_with("Task was not saved. Something went wrong. Try again.")

    def test_create_new_task_created(self):
        with patch.object(self.controller.view, "prompt_user_question", return_value="New task"):
            self.controller.create_new_task(self.main_controller)

            with self.controller.model.database(TestDatabaseConnection.database_path) as connection:
                cursor = connection.cursor()
                task = cursor.execute("SELECT * FROM tasks").fetchall()

            self.assertTrue(task)
            self.assertEqual("New task", task[0]["task_name"])
            self.assertEqual("Not started", task[0]["status"])

    def test_display_all_tasks(self):
        with self.controller.model.database(TestDatabaseConnection.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tasks(task_name, user_id) VALUES('first task', 1)")

        with patch.object(self.controller.model, "get_all_tasks"), \
            patch.object(self.controller.view, "display_list_tasks"):

            result = self.controller.display_all_tasks(self.main_controller)
            
            self.assertTrue(result)
            self.controller.view.display_list_tasks.assert_called_once()

    @patch("builtins.print")
    def test_display_all_tasks_func_called(self, mocked_print):
        with patch.object(self.controller.model, "get_all_tasks"), \
            patch.object(self.controller.view, "display_list_tasks"):

            self.controller.display_all_tasks(self.main_controller)

            self.controller.model.get_all_tasks.assert_called_once_with(user_id=self.main_controller.user_id)
            self.controller.view.display_list_tasks.assert_called_once()

    @patch("builtins.input")
    def test_update_task(self, mocked_input):
        with patch.object(self.controller, "get_and_validate_task_id", return_value=1) as mocked_validate_task_id, \
            patch.object(self.controller.model, "get_task_id", return_value=1), \
            patch.object(self.controller.model, "update"):
            mocked_input.return_value = "Task updated"

            result = self.controller.update_task(self.main_controller)

            self.assertTrue(result)
            mocked_validate_task_id.assert_called_once()
            mocked_input.assert_called_once_with("New task name: ")
            self.controller.model.get_task_id.assert_called_once_with(user_id=self.main_controller.user_id, task_id=1)
            self.controller.model.update.assert_called_once_with(user_id=self.main_controller.user_id, task_id=1, new_task="Task updated")
            self.controller.view.info.assert_called_once_with("Task updated!")

    def test_update_task_id_invalid(self):
        with patch.object(self.controller, "get_and_validate_task_id", return_value=False):
            result = self.controller.update_task(self.main_controller)

        self.assertFalse(result)

    def test_delete_task(self):
        with patch.object(self.controller, "get_and_validate_task_id", return_value=1) as mocked_validate_task_id, \
            patch.object(self.controller.model, "get_task_id", return_value=1), \
            patch.object(self.controller.model, "delete"):

            result = self.controller.delete_task(self.main_controller)

            self.assertTrue(result)
            mocked_validate_task_id.assert_called_once_with(user_id=self.main_controller.user_id)
            self.controller.model.get_task_id.assert_called_once_with(user_id=self.main_controller.user_id, task_id=1)
            self.controller.model.delete.assert_called_once_with(user_id=self.main_controller.user_id, task_id=1)
            self.controller.view.info.assert_called_once_with("Task with id '1' deleted.")

    def test_delete_task_id_invalid(self):
        with patch.object(self.controller, "get_and_validate_task_id", return_value=False):
            result = self.controller.delete_task(self.main_controller)

        self.assertFalse(result)

    @patch("builtins.input")
    def test_get_and_validate_task_id(self, mocked_input):
        with patch.object(self.controller.model, "get_all_tasks", return_value=[1, 2]):
            mocked_input.return_value = "1"

            result = self.controller.get_and_validate_task_id(user_id=self.main_controller.user_id)

            self.assertEqual(result, 1)

    def test_get_and_validate_task_id_no_tasks(self):
        with patch.object(self.controller.model, "get_all_tasks", return_value=False):
            result = self.controller.get_and_validate_task_id(user_id=self.main_controller.user_id)

            self.assertFalse(result)
            self.controller.view.error.assert_called_once_with("You don't have any tasks.")

    @patch("builtins.input")
    def test_get_and_validate_task_id_input_letter(self, mocked_input):
        with patch.object(self.controller.model, "get_all_tasks", return_value=[1, 2]):
            mocked_input.return_value = "a"

            result = self.controller.get_and_validate_task_id(user_id=self.main_controller.user_id)

            self.assertFalse(result)
            self.controller.view.error.assert_called_once_with("Task id must be a number")

    @patch("builtins.input")
    def test_get_and_validate_task_id_nonexisting_task(self, mocked_input):
        with patch.object(self.controller.model, "get_all_tasks", return_value=[1, 2]):
            mocked_input.return_value = "4"

            result = self.controller.get_and_validate_task_id(user_id=self.main_controller.user_id)

            self.assertFalse(result)
            self.controller.view.error.assert_called_once_with("We couldn't find a task with the id of '4'")
