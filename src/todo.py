"""极简待办清单（命令行版）。

用法：
    python src/todo.py list
    python src/todo.py add <任务标题>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks(path: Path = DATA_FILE) -> list[dict]:
    """从 JSON 文件读取任务列表；文件不存在时视为空列表。"""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict], path: Path = DATA_FILE) -> None:
    """把任务列表写回 JSON 文件（UTF-8，保留中文原样）。"""
    text = json.dumps(tasks, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def add_task(tasks: list[dict], title: str) -> list[dict]:
    """追加一条未完成的任务。"""
    tasks.append({"title": title, "done": False})
    return tasks


def list_tasks(tasks: list[dict]) -> str:
    """把任务列表渲染成人类可读的多行文本，序号从 1 开始。"""
    if not tasks:
        return "（暂无待办）"
    lines = []
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        lines.append(f"{number}. [{mark}] {task['title']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    tasks = load_tasks()

    if not argv or argv[0] == "list":
        print(list_tasks(tasks))
        return 0

    if argv[0] == "add":
        if len(argv) < 2:
            print("用法：python src/todo.py add <任务标题>")
            return 2
        add_task(tasks, argv[1])
        save_tasks(tasks)
        print(f"已添加：{argv[1]}")
        return 0

    print(f"未知命令：{argv[0]}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
