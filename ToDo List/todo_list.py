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

