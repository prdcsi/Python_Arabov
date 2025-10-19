from abc import ABC, abstractmethod
from car import Car

class PriceChangeHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, car: Car, new_price: float, user_role: str) -> bool:
        pass


class SalesManager(PriceChangeHandler):
    def handle(self, car: Car, new_price: float, user_role: str) -> bool:
        if abs(car.price - new_price) / car.price <= 0.05:  # ±5%
            car.price = new_price
            print("Менеджер одобрил изменение цены")
            return True
        elif self._next_handler:
            return self._next_handler.handle(car, new_price, user_role)
        return False


class FinanceDepartment(PriceChangeHandler):
    def handle(self, car: Car, new_price: float, user_role: str) -> bool:
        if abs(car.price - new_price) / car.price <= 0.2:  # ±20%
            car.price = new_price
            print("Финансовый отдел одобрил изменение цены")
            return True
        elif self._next_handler:
            return self._next_handler.handle(car, new_price, user_role)
        return False


class Director(PriceChangeHandler):
    def handle(self, car: Car, new_price: float, user_role: str) -> bool:
        car.price = new_price
        print("Директор одобрил изменение цены")
        return True