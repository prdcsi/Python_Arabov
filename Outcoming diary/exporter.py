import csv
from database import get_all_expenses


def export_to_csv(filename="expenses.csv"):
    """Экспортирует все расходы в CSV-файл."""
    expenses = get_all_expenses()
    if not expenses:
        print("Нет данных для экспорта.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Заголовки
        writer.writerow(["ID", "Сумма", "Категория", "Дата", "Описание"])
        # Данные
        writer.writerows(expenses)

    print(f"✅ Данные экспортированы в {filename}")