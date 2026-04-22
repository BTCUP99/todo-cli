# todo-cli

命令行待办事项管理工具，简单易用的 Todo 应用。

## 功能介绍

- ✅ **添加待办** - 创建新的待办事项
- 📋 **列出待办** - 查看所有/待完成/已完成的待办
- ✔️ **完成待办** - 标记待办事项为已完成
- 🗑️ **删除待办** - 删除不需要的待办事项
- 💾 **持久化存储** - JSON 文件本地存储

## 使用方法

### 基本命令

```bash
# 添加待办事项
python todo.py add <内容>

# 列出所有待办
python todo.py list

# 列出待完成的待办
python todo.py list pending

# 列出已完成的待办
python todo.py list completed

# 完成待办事项
python todo.py done <ID>

# 删除待办事项
python todo.py delete <ID>

# 显示帮助
python todo.py help
```

### 示例

```bash
# 添加待办
python todo.py add 买早餐
python todo.py add 完成项目报告

# 查看列表
python todo.py list

# 完成待办（假设 ID 为 1）
python todo.py done 1

# 删除待办（假设 ID 为 2）
python todo.py delete 2
```

## 数据存储

待办事项存储在 `~/.todo_cli/todos.json` 文件中。

## 系统要求

- Python 3.6+

## 许可证

MIT License
