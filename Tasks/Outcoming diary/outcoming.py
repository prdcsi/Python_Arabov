from database import init_db, add_expense, get_all_expenses, get_expenses_by_date, get_expenses_by_category
from exporter import export_to_csv


def print_expenses(expenses):
    if not expenses:
        print("Записей не найдено.")
        return
    print(f"{'ID':<4} {'Сумма':<10} {'Категория':<15} {'Дата':<12} {'Описание'}")
    print("-" * 60)
    for row in expenses:
        print(f"{row[0]:<4} {row[1]:<10} {row[2]:<15} {row[3]:<12} {row[4] or ''}")


def main():
    init_db()
    while True:
        print("\n=== Дневник расходов ===")
        print("1. Добавить расход")
        print("2. Показать все расходы")
        print("3. Показать расходы по дате")
        print("4. Показать расходы по категории")
        print("5. Экспортировать в CSV")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            try:
                amount = float(input("Введите сумму: "))
                category = input("Введите категорию (еда, транспорт, развлечения, другие): ").strip()
                date = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
                description = input("Описание (опционально): ").strip()
                add_expense(amount, category, date, description)
                print("✅ Расход добавлен!")
            except ValueError as e:
                print(f"❌ Ошибка: {e}")
            except Exception as e:
                print(f"❌ Неизвестная ошибка: {e}")

        elif choice == "2":
            expenses = get_all_expenses()
            print_expenses(expenses)

        elif choice == "3":
            date = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
            expenses = get_expenses_by_date(date)
            print_expenses(expenses)

        elif choice == "4":
            category = input("Введите категорию: ").strip()
            expenses = get_expenses_by_category(category)
            print_expenses(expenses)

        elif choice == "5":
            export_to_csv()

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()