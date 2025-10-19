import logging
from car_factory import CarFactory
from customer import Customer
from dealership import Dealership
from handlers import SalesManager, FinanceDepartment, Director
from sale import OnlineSaleProcess

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

    # Создание автомобилей
    sedan = CarFactory.create_car("sedan", car_id="C001", make="Toyota", model="Camry", year=2023, price=25000, fuel_efficiency=6.5)
    suv = CarFactory.create_car("suv", car_id="C002", make="Ford", model="Explorer", year=2024, price=40000, towing_capacity=2500)
    ev = CarFactory.create_car("electric", car_id="C003", make="Tesla", model="Model 3", year=2025, price=45000, battery_range=500)

    dealership.add_car(sedan)
    dealership.add_car(suv)
    dealership.add_car(ev)

    # Создание клиента
    customer = Customer("CU001", "Иван Петров", "+79991234567")

    # Продажа
    sale_process = OnlineSaleProcess()
    sale = sale_process.sell_car(sedan, customer)
    dealership.sales.append(sale)

    # Поиск
    print("\n=== Все автомобили ===")
    for car in dealership.get_all_cars():
        print(car)

    print("\n=== Поиск по марке 'Toyota' ===")
    for car in dealership.search_by_make("Toyota"):
        print(car)

    # Изменение цены через цепочку
    chain = SalesManager(FinanceDepartment(Director()))
    try:
        dealership.change_car_price("C002", 38000, user_role="manager", handler=chain)
        print(f"Новая цена Ford Explorer: {suv.price}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # Сохранение
    dealership.save_to_file()

if __name__ == "__main__":
    main()