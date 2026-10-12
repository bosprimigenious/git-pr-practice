"""todo.py 的最小单元测试。

运行：python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import todo  # noqa: E402


class TodoTest(unittest.TestCase):
    def test_add_task_appends_unfinished_item(self):
        tasks = todo.add_task([], "写实验报告")
        self.assertEqual(tasks, [{"title": "写实验报告", "done": False}])

    def test_list_tasks_numbers_from_one(self):
        tasks = [{"title": "A", "done": False}, {"title": "B", "done": True}]
        self.assertEqual(todo.list_tasks(tasks), "1. [ ] A\n2. [x] B")

    def test_list_tasks_empty(self):
        self.assertEqual(todo.list_tasks([]), "（暂无待办）")

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            todo.save_tasks([{"title": "中文标题", "done": False}], path)
            self.assertEqual(todo.load_tasks(path), [{"title": "中文标题", "done": False}])

    def test_done_task_marks_correct_item(self):
        tasks = [
            {"title": "任务A", "done": False},
            {"title": "任务B", "done": False},
        ]

        result = todo.done_task(tasks, 1)

        self.assertTrue(result)
        self.assertTrue(tasks[0]["done"])
        self.assertFalse(tasks[1]["done"])

    def test_done_task_rejects_out_of_range(self):
        tasks = [{"title": "任务A", "done": False}]

        self.assertFalse(todo.done_task(tasks, 2))
        self.assertFalse(todo.done_task(tasks, 0))
        self.assertFalse(todo.done_task(tasks, -1))

        # 错误操作不应改变任务状态
        self.assertFalse(tasks[0]["done"])

    def test_cli_done_rejects_bad_input(self):
        cases = (
            ["done"],
            ["done", "abc"],
            ["done", "9999"],
            ["done", "0"],
        )

        for argv in cases:
            with self.subTest(argv=argv):
                tasks = [{"title": "任务A", "done": False}]
                output = StringIO()

                with patch.object(todo, "load_tasks", return_value=tasks):
                    with patch.object(todo, "save_tasks") as mock_save:
                        with redirect_stdout(output):
                            result = todo.main(argv)

                self.assertEqual(result, 2)
                self.assertFalse(tasks[0]["done"])
                mock_save.assert_not_called()

    def test_done_task_persists_to_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            tasks = [
                {"title": "任务A", "done": False},
                {"title": "任务B", "done": False},
            ]

            todo.save_tasks(tasks, path)

            loaded = todo.load_tasks(path)
            self.assertTrue(todo.done_task(loaded, 1))
            todo.save_tasks(loaded, path)

            saved = todo.load_tasks(path)
            self.assertTrue(saved[0]["done"])
            self.assertFalse(saved[1]["done"])
            self.assertEqual(
                todo.list_tasks(saved),
                "1. [x] 任务A\n2. [ ] 任务B"
            )

    def test_cli_done_already_completed(self):
        tasks = [{"title": "任务A", "done": True}]
        output = StringIO()

        with patch.object(todo, "load_tasks", return_value=tasks):
            with patch.object(todo, "save_tasks") as mock_save:
                with redirect_stdout(output):
                    result = todo.main(["done", "1"])

        self.assertEqual(result, 0)
        self.assertIn("本来就是已完成状态", output.getvalue())
        mock_save.assert_not_called()

if __name__ == "__main__":
    unittest.main()
