import json
import os
from typing import List, Optional
from car import Car
from customer import Customer
from sale import Sale
from exceptions import SaleNotFoundError
from decorators import check_permissions

class Dealership:
    def __init__(self, name: str):
        self.name = name
        self.cars: List[Car] = []
        self.sales: List[Sale] = []

    def add_car(self, car: Car):
        self.cars.append(car)

    def remove_car(self, car_id: str):
        self.cars = [c for c in self.cars if c.car_id != car_id]

    def get_all_cars(self) -> List[Car]:
        return self.cars

    def search_by_make(self, make: str) -> List[Car]:
        return [car for car in self.cars if car.make.lower() == make.lower()]

    def find_sale(self, sale_id: str) -> Optional[Sale]:
        for sale in self.sales:
            if sale.sale_id == sale_id:
                return sale
        raise SaleNotFoundError(f"Продажа {sale_id} не найдена")

    @check_permissions("manager")
    def change_car_price(self, car_id: str, new_price: float, user_role: str, handler):
        car = next((c for c in self.cars if c.car_id == car_id), None)
        if not car:
            raise InvalidCarError("Автомобиль не найден")
        if not handler.handle(car, new_price, user_role):
            raise PermissionDeniedError("Изменение цены не одобрено")

    def save_to_file(self, filename: str = "dealership.json"):
        data = {
            "cars": [car.to_dict() for car in self.cars],
            "sales": [sale.to_dict() for sale in self.sales]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str = "dealership.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.cars = [Car.from_dict(car) for car in data["cars"]]
        self.sales = [Sale.from_dict(sale) for sale in data["sales"]]