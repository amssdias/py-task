import unittest
from unittest.mock import patch

from colorama import Fore

from apps.todotasks.view import TodoView


class TestTodoView(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.view = TodoView()
        return super().setUpClass()

    @patch("builtins.input", return_value="testing")
    def test_prompt_user_question_input_called(self, mocked_input):
        
        result = self.view.prompt_user_question("Some question")

        self.assertEqual("testing", result)
        mocked_input.assert_called_once_with(Fore.GREEN + "Some question")

    @patch("builtins.print")
    def test_info_print_called(self, mocked_print):
        result = self.view.info("info")

        self.assertEqual(None, result)
        mocked_print.assert_called_once_with(Fore.CYAN + "info")

    @patch("builtins.print")
    def test_error_print_called(self, mocked_print):
        result = self.view.error("error")

        self.assertEqual(None, result)
        mocked_print.assert_called_once_with(Fore.RED + "error")

    def test_display_list_tasks_info_called(self):
        with patch.object(self.view, "info") as mocked_info:
            result = self.view.display_list_tasks([])

        self.assertEqual(None, result)
        mocked_info.assert_called_once_with("There are no tasks yet, create a few first.")
        mocked_info.asser

    @patch("builtins.print")
    def test_display_list_tasks_print_called(self, mocked_print):
        result = self.view.display_list_tasks(["First task", "Second task"])

        self.assertEqual(None, result)
        mocked_print.assert_called()