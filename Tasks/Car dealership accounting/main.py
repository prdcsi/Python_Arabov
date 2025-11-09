# main.py
import logging
import os
from car_factory import CarFactory
from dealership import Dealership
from exceptions import InvalidCarError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dealership.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def main():
    dealership = Dealership("Автоцентр 'Премиум'")
    dealership.load_from_file()

    print("🚗 Добро пожаловать в систему управления автосалоном!")
    while True:
        print("\n=== Меню ===")
        print("1. Добавить автомобиль")
        print("2. Показать все автомобили")
        print("3. Найти автомобили по марке")
        print("4. Удалить автомобиль")
        print("5. Изменить цену автомобиля")
        print("6. Продать автомобиль")
        print("7. Сохранить данные")
        print("0. Выйти")

        choice = input("\nВыберите действие: ").strip()

        try:
            if choice == "1":
                print("\nТипы: sedan, suv, electric")
                car_type = input("Тип автомобиля: ").strip().lower()
                car_id = input("ID автомобиля: ").strip()
                make = input("Марка: ").strip()
                model = input("Модель: ").strip()
                year = int(input("Год выпуска: "))
                price = float(input("Цена: "))

                if car_type == "sedan":
                    fuel = float(input("Расход топлива (л/100км): "))
                    car = CarFactory.create_car(car_type, car_id=car_id, make=make, model=model, year=year, price=price, fuel_efficiency=fuel)
                elif car_type == "suv":
                    tow = float(input("Грузоподъемность (кг): "))
                    car = CarFactory.create_car(car_type, car_id=car_id, make=make, model=model, year=year, price=price, towing_capacity=tow)
                elif car_type == "electric":
                    rng = float(input("Запас хода (км): "))
                    car = CarFactory.create_car(car_type, car_id=car_id, make=make, model=model, year=year, price=price, battery_range=rng)
                else:
                    print("❌ Неизвестный тип.")
                    continue

                dealership.add_car(car)

            elif choice == "2":
                cars = dealership.get_all_cars()
                if not cars:
                    print("📭 Нет доступных автомобилей.")
                else:
                    for car in cars:
                        print(f"  • {car} → Цена: {car.calculate_price():,.0f} руб.")

            elif choice == "3":
                make = input("Введите марку: ").strip()
                cars = dealership.search_by_make(make)
                if not cars:
                    print(f"📭 Нет автомобилей марки {make}.")
                else:
                    for car in cars:
                        print(f"  • {car}")

            elif choice == "4":
                car_id = input("ID автомобиля для удаления: ").strip()
                dealership.remove_car(car_id)

            elif choice == "5":
                car_id = input("ID автомобиля: ").strip()
                new_price = float(input("Новая цена: "))
                dealership.edit_car_price(car_id, new_price)

            elif choice == "6":
                car_id = input("ID автомобиля: ").strip()
                name = input("Имя клиента: ").strip()
                phone = input("Телефон клиента: ").strip()
                dealership.sell_car(car_id, name, phone)

            elif choice == "7":
                dealership.save_to_file()

            elif choice == "0":
                dealership.save_to_file()
                print("🚪 До свидания!")
                break

            else:
                print("❌ Неверный выбор.")

        except ValueError as e:
            print(f"❌ Ошибка ввода: {e}")
        except InvalidCarError as e:
            print(f"❌ Ошибка автомобиля: {e}")
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")

if __name__ == "__main__":
    main()