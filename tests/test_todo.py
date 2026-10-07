"""todo.py 的最小单元测试。

运行：python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
