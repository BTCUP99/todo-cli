#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行待办事项管理工具
功能：添加、列出、完成、删除待办事项
数据存储：JSON 文件持久化
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

TODO_FILE = Path.home() / ".todo_cli" / "todos.json"


def load_todos():
    """加载待办事项"""
    if not TODO_FILE.exists():
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_todos(todos):
    """保存待办事项"""
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(title):
    """添加待办事项"""
    todos = load_todos()
    todo_id = max([t["id"] for t in todos], default=0) + 1
    todo = {
        "id": todo_id,
        "title": title,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    todos.append(todo)
    save_todos(todos)
    print(f"✓ 已添加待办事项 [{todo_id}] {title}")


def list_todos(status="all"):
    """列出待办事项"""
    todos = load_todos()

    if status == "pending":
        todos = [t for t in todos if not t["completed"]]
        title = "待完成的待办事项"
    elif status == "completed":
        todos = [t for t in todos if t["completed"]]
        title = "已完成的待办事项"
    else:
        title = "所有待办事项"

    print(f"\n{'='*50}")
    print(f"  {title} (共 {len(todos)} 项)")
    print(f"{'='*50}")

    if not todos:
        print("  (暂无待办事项)")
    else:
        for i, todo in enumerate(todos, 1):
            status_icon = "✓" if todo["completed"] else "○"
            title_text = todo["title"]
            if todo["completed"]:
                title_text = f"\033[9m{title_text}\033[0m"  # 删除线
            print(f"  {i}. [{status_icon}] {title_text}")

    print(f"{'='*50}\n")


def complete_todo(todo_id):
    """完成待办事项"""
    todos = load_todos()
    found = False

    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            todo["completed_at"] = datetime.now().isoformat()
            found = True
            print(f"✓ 已完成 [{todo_id}] {todo['title']}")
            break

    if not found:
        print(f"✗ 未找到 ID 为 {todo_id} 的待办事项")
        return

    save_todos(todos)


def delete_todo(todo_id):
    """删除待办事项"""
    todos = load_todos()
    initial_len = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]

    if len(todos) == initial_len:
        print(f"✗ 未找到 ID 为 {todo_id} 的待办事项")
        return

    save_todos(todos)
    print(f"✓ 已删除待办事项 [{todo_id}]")


def print_help():
    """打印帮助信息"""
    help_text = """
╔══════════════════════════════════════════════════════╗
║           命令行待办事项管理工具 v1.0.3               ║
╠══════════════════════════════════════════════════════╣
║  使用方法:                                            ║
║    python todo.py add <内容>      添加待办事项        ║
║    python todo.py list            列出所有待办        ║
║    python todo.py list pending    列出待完成项        ║
║    python todo.py list completed  列出已完成项        ║
║    python todo.py done <ID>       完成待办事项        ║
║    python todo.py delete <ID>     删除待办事项        ║
║    python todo.py help            显示帮助信息        ║
╠══════════════════════════════════════════════════════╣
║  示例:                                                ║
║    python todo.py add 买早餐                           ║
║    python todo.py list                                 ║
║    python todo.py done 1                              ║
║    python todo.py delete 2                             ║
╚══════════════════════════════════════════════════════╝
"""
    print(help_text)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "add" and len(sys.argv) >= 3:
        title = " ".join(sys.argv[2:])
        add_todo(title)

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else "all"
        list_todos(status)

    elif command in ("done", "complete", "finish") and len(sys.argv) >= 3:
        try:
            todo_id = int(sys.argv[2])
            complete_todo(todo_id)
        except ValueError:
            print("✗ 请提供有效的待办事项 ID")

    elif command in ("delete", "remove", "rm") and len(sys.argv) >= 3:
        try:
            todo_id = int(sys.argv[2])
            delete_todo(todo_id)
        except ValueError:
            print("✗ 请提供有效的待办事项 ID")

    elif command in ("help", "--help", "-h"):
        print_help()

    else:
        print(f"✗ 未知命令: {command}")
        print("  运行 'python todo.py help' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
