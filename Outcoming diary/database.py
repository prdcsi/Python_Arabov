import sqlite3
from datetime import datetime


def init_db():
    """Создаёт таблицу expenses, если её нет."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_expense(amount, category, date, description=""):
    """Добавляет запись о расходе."""
    # Валидация даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, date, description))
    conn.commit()
    conn.close()


def get_all_expenses():
    """Возвращает все расходы."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_date(target_date):
    """Возвращает расходы по дате."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE date = ?', (target_date,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_category(category):
    """Возвращает расходы по категории."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows