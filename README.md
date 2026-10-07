# 极简待办清单 (todo-cli)

一个用来练习 Git 协作流程的小型 Python 命令行项目：远程仓库、分支、Pull Request、
代码评审、合并。

## 功能

| 命令 | 说明 |
| --- | --- |
| `python src/todo.py list` | 列出全部待办（默认命令） |
| `python src/todo.py add <标题>` | 添加一条待办 |

任务数据保存在当前目录的 `tasks.json`（UTF-8，不转义中文）。

## 使用示例

```bash
python src/todo.py add "写程序设计实践实验报告"
python src/todo.py list
```

输出：

```
1. [ ] 写程序设计实践实验报告
```

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 协作约定

- `main` 分支受保护思路：任何人都不要直接往 `main` 推送功能改动，一律走
  `feature/<名字>` 分支 + Pull Request。
- 每个 PR 至少需要一名 reviewer 评审通过后才能合并。
