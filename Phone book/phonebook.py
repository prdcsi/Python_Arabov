import sqlite3
from typing import List, Dict, Optional


DB_NAME = "phonebook.db"


def init_db():
    """Создаёт таблицу contacts, если её нет."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT
            )
        """)
        conn.commit()


