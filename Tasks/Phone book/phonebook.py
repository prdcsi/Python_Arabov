import sqlite3
import json
import csv
import os
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

def export_to_json(filename: str = "contacts.json"):
    contacts = get_all_contacts()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)
    print(f"Экспорт в {filename} завершён.")


def export_to_csv(filename: str = "contacts.csv"):
    contacts = get_all_contacts()
    if not contacts:
        print("Нет контактов для экспорта.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "phone", "email"])
        writer.writeheader()
        writer.writerows(contacts)
    print(f"Экспорт в {filename} завершён.")


def import_from_json(filename: str = "contacts.json"):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Ошибка: файл повреждён или не является JSON.")
            return

    added = 0
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for item in data:
            name = item.get("name")
            phone = item.get("phone")
            email = item.get("email")
            if name and phone:
                cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
                added += 1
        conn.commit()
    print(f"Импортировано {added} контактов из {filename}.")


def import_from_csv(filename: str = "contacts.csv"):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return

    added = 0
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            for row in reader:
                name = row.get("name")
                phone = row.get("phone")
                email = row.get("email") or None
                if name and phone:
                    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
                    added += 1
            conn.commit()
    print(f"Импортировано {added} контактов из {filename}.")

def show_menu():
    print("\n=== Телефонная книга ===")
    print("1. Добавить контакт")
    print("2. Показать все контакты")
    print("3. Редактировать контакт")
    print("4. Удалить контакт")
    print("5. Экспорт в JSON")
    print("6. Экспорт в CSV")
    print("7. Импорт из JSON")
    print("8. Импорт из CSV")
    print("0. Выход")
    return input("Выберите действие: ")


def main():
    init_db()

    while True:
        choice = show_menu()

        if choice == '0':
            print("Выход из программы.")
            break

        elif choice == '1':
            name = input("Имя: ").strip()
            phone = input("Телефон: ").strip()
            email = input("Email (опционально): ").strip() or None
            if name and phone:
                add_contact(name, phone, email)
            else:
                print("Имя и телефон обязательны.")

        elif choice == '2':
            show_contacts()

        elif choice == '3':
            try:
                contact_id = int(input("ID контакта для редактирования: "))
                name = input("Новое имя: ").strip()
                phone = input("Новый телефон: ").strip()
                email = input("Новый email (опционально): ").strip() or None
                if name and phone:
                    update_contact(contact_id, name, phone, email)
                else:
                    print("Имя и телефон обязательны.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")

        elif choice == '4':
            try:
                contact_id = int(input("ID контакта для удаления: "))
                delete_contact(contact_id)
            except ValueError:
                print("Ошибка: ID должен быть числом.")

        elif choice == '5':
            filename = input("Имя файла для экспорта в JSON (по умолчанию: contacts.json): ").strip() or "contacts.json"
            export_to_json(filename)

        elif choice == '6':
            filename = input("Имя файла для экспорта в CSV (по умолчанию: contacts.csv): ").strip() or "contacts.csv"
            export_to_csv(filename)

        elif choice == '7':
            filename = input("Имя JSON-файла для импорта (по умолчанию: contacts.json): ").strip() or "contacts.json"
            import_from_json(filename)

        elif choice == '8':
            filename = input("Имя CSV-файла для импорта (по умолчанию: contacts.csv): ").strip() or "contacts.csv"
            import_from_csv(filename)

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
