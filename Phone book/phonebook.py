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


def add_contact(name: str, phone: str, email: Optional[str] = None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        print("Контакт добавлен.")


def get_all_contacts() -> List[Dict]:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row  # позволяет обращаться по имени столбца
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        return [dict(row) for row in cursor.fetchall()]


def update_contact(contact_id: int, name: str, phone: str, email: Optional[str] = None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
            (name, phone, email, contact_id)
        )
        if cursor.rowcount == 0:
            print("Контакт с таким ID не найден.")
        else:
            conn.commit()
            print("Контакт обновлён.")


def delete_contact(contact_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        if cursor.rowcount == 0:
            print("Контакт с таким ID не найден.")
        else:
            conn.commit()
            print("Контакт удалён.")



def show_contacts():
    contacts = get_all_contacts()
    if not contacts:
        print("Телефонная книга пуста.")
        return

    print("\n--- Все контакты ---")
    for c in contacts:
        email_str = f", email: {c['email']}" if c['email'] else ""
        print(f"ID: {c['id']} | Имя: {c['name']} | Телефон: {c['phone']}{email_str}")


