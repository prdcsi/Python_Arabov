import sqlite3
from datetime import datetime
import sys

DB_NAME = "tasks.db"

def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_task(description):
    """Добавление новой задачи."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (description, created_at) VALUES (?, ?)", (description, now))
    conn.commit()
    conn.close()
    print("✅ Задача добавлена.")

def list_tasks():
    """Вывод всех задач."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, created_at, is_done FROM tasks ORDER BY id")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("📭 Список задач пуст.")
        return

    print("\n📋 Список задач:")
    for task in tasks:
        status = "[x]" if task[3] else "[ ]"
        print(f"{status} {task[0]}. {task[1]} (создано: {task[2]})")
    print()

def mark_done(task_id):
    """Отметить задачу как выполненную."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        print("❌ Задача с таким ID не найдена.")
    else:
        print("✅ Задача отмечена как выполненная.")
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Удалить задачу по ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        print("❌ Задача с таким ID не найдена.")
    else:
        print("🗑️ Задача удалена.")
    conn.commit()
    conn.close()

def show_help():
    """Показать справку."""
    print("""
🔧 Доступные команды:
  add "текст задачи"   — добавить новую задачу
  list                 — показать все задачи
  done <id>            — отметить задачу как выполненную
  delete <id>          — удалить задачу
  help                 — показать эту справку
  exit                 — выйти из программы
    """)

def main():
    init_db()
    print("🚀 Добро пожаловать в Менеджер задач!")
    show_help()

    while True:
        try:
            user_input = input(">>> ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()

            if command == "exit":
                print("👋 До встречи!")
                break
            elif command == "help":
                show_help()
            elif command == "list":
                list_tasks()
            elif command == "add":
                if len(parts) < 2:
                    print("❗ Укажите описание задачи: add \"ваша задача\"")
                else:
                    add_task(parts[1].strip('"'))
            elif command == "done":
                if len(parts) < 2 or not parts[1].isdigit():
                    print("❗ Укажите корректный ID задачи: done 1")
                else:
                    mark_done(int(parts[1]))
            elif command == "delete":
                if len(parts) < 2 or not parts[1].isdigit():
                    print("❗ Укажите корректный ID задачи: delete 1")
                else:
                    delete_task(int(parts[1]))
            else:
                print("❓ Неизвестная команда. Введите 'help' для справки.")
        except KeyboardInterrupt:
            print("\n👋 Принудительный выход.")
            sys.exit(0)
        except Exception as e:
            print(f"💥 Ошибка: {e}")

if __name__ == "__main__":
    main()