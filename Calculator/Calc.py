def show_menu():
    print("\n=== Калькулятор ===")
    print("1. Сложение (+)")
    print("2. Вычитание (-)")
    print("3. Умножение (*)")
    print("4. Деление (/)")
    print("5. Возведение в степень (**)")
    print("6. Остаток от деления (%)")
    print("7. Целочисленное деление (//)")
    print("8. Показать историю")
    print("9. Очистить историю")
    print("0. Выход")
    choice = input("Выберите действие: ")
    return choice


def get_numbers():
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))
        return a, b
    except ValueError:
        print("Ошибка: введите корректные числа.")
        return None, None


def perform_operation(choice, a, b):
    operations = {
        '1': lambda x, y: x + y,
        '2': lambda x, y: x - y,
        '3': lambda x, y: x * y,
        '4': lambda x, y: x / y if y != 0 else None,
        '5': lambda x, y: x ** y,
        '6': lambda x, y: x % y if y != 0 else None,
        '7': lambda x, y: x // y if y != 0 else None,
    }

    op_symbols = {
        '1': '+',
        '2': '-',
        '3': '*',
        '4': '/',
        '5': '**',
        '6': '%',
        '7': '//',
    }

    if choice not in operations:
        return None, None

    try:
        result = operations[choice](a, b)
        if result is None:
            return "Ошибка: деление на ноль!", None
        symbol = op_symbols[choice]
        return f"{a} {symbol} {b} = {result}", result
    except (ZeroDivisionError, ValueError, OverflowError) as e:
        return f"Ошибка вычисления: {e}", None


def main():
    history = []

    while True:
        choice = show_menu()

        if choice == '0':
            print("Выход из программы. До свидания!")
            break

        elif choice in ['1', '2', '3', '4', '5', '6', '7']:
            a, b = get_numbers()
            if a is None or b is None:
                continue  # повторить ввод

            expression, result = perform_operation(choice, a, b)
            if result is not None:
                print(f"Результат: {expression}")
                history.append(expression)
            else:
                print(expression)  # сообщение об ошибке

        elif choice == '8':
            if history:
                print("\n--- История операций ---")
                for i, record in enumerate(history, 1):
                    print(f"{i}. {record}")
            else:
                print("История пуста.")

        elif choice == '9':
            history.clear()
            print("История очищена.")

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт из меню.")


if __name__ == "__main__":
    main()