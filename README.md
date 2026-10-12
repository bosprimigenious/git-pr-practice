# 极简待办清单 (todo-cli)

一个用来练习 Git 协作流程的小型 Python 命令行项目：远程仓库、分支、Pull Request、
代码评审、合并。

## 功能

| 命令 | 说明 |
| --- | --- |
| `python src/todo.py list` | 列出全部待办（默认命令） |
| `python src/todo.py add <标题>` | 添加一条待办 |
| `python src/todo.py done <序号>` | 将指定序号的待办标记为已完成 |

任务数据保存在当前目录的 `tasks.json`（UTF-8，不转义中文）。


## 使用示例

添加待办任务：

```bash
python src/todo.py add "写程序设计实践实验报告"
python src/todo.py add "复习离散数学"
```

查看任务：

```bash
python src/todo.py list
```

输出：

```text
1. [ ] 写程序设计实践实验报告
2. [ ] 复习离散数学
```

将第一条任务标记为已完成：

```bash
python src/todo.py done 1
```

输出：

```text
已完成第 1 条任务：写程序设计实践实验报告
```

再次查看：

```bash
python src/todo.py list
```

输出：

```text
1. [x] 写程序设计实践实验报告
2. [ ] 复习离散数学
```

注意：
- 序号从 1 开始。
- 如果任务列表为空，会提示先添加任务。
- 如果序号超出范围，程序会提示合法范围。
- 如果任务已经完成，再次执行 done 不会重复修改。
- 缺少参数或输入无效序号时，程序会返回错误退出码 2。


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
