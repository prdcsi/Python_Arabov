from datetime import datetime
from typing import List
from interfaces import Sellable, Reportable
from mixins import LoggingMixin, NotificationMixin
from customer import Customer
from car import Car

class Sale(LoggingMixin, NotificationMixin):
    def __init__(self, sale_id: str, customer: Customer, car: Car, sale_date: datetime = None):
        self.sale_id = sale_id
        self.customer = customer
        self.car = car
        self.sale_date = sale_date or datetime.now()
        self.accessories: List[str] = []
        self.total_price = self.calculate_total()

    def add_accessory(self, accessory: str):
        self.accessories.append(accessory)
        self.total_price = self.calculate_total()

    def remove_accessory(self, accessory: str):
        if accessory in self.accessories:
            self.accessories.remove(accessory)
            self.total_price = self.calculate_total()

    def calculate_total(self) -> float:
        base = self.car.calculate_price()
        return base + len(self.accessories) * 1000  # 1000 за аксессуар

    def __str__(self) -> str:
        return f"Продажа #{self.sale_id}: {self.car} клиенту {self.customer.name}"

    def to_dict(self) -> dict:
        return {
            "sale_id": self.sale_id,
            "customer": self.customer.to_dict(),
            "car": self.car.to_dict(),
            "sale_date": self.sale_date.isoformat(),
            "accessories": self.accessories,
            "total_price": self.total_price
        }

    @classmethod
    def from_dict(cls, data: dict):
        customer = Customer.from_dict(data["customer"])
        car = Car.from_dict(data["car"])
        sale_date = datetime.fromisoformat(data["sale_date"])
        sale = cls(data["sale_id"], customer, car, sale_date)
        sale.accessories = data["accessories"]
        sale.total_price = data["total_price"]
        return sale


class SaleProcess(Reportable, Sellable, LoggingMixin, NotificationMixin):
    def sell_car(self, car: Car, customer: Customer):
        if not car.is_available:
            raise InvalidCarError("Автомобиль недоступен для продажи")
        car.is_available = False
        sale = Sale(sale_id=f"S{hash(car.car_id) % 10000}", customer=customer, car=car)
        self.log_action(f"Продажа {sale.sale_id} оформлена")
        self.send_notification(f"Ваш автомобиль {car.make} {car.model} готов к выдаче")
        return sale

    def generate_report(self) -> str:
        return "Отчет по продаже: данные отсутствуют (реализуется в подклассах)"


class OnlineSaleProcess(SaleProcess):
    def sell_car(self, car: Car, customer: Customer):
        sale = super().sell_car(car, customer)
        self.log_action("Онлайн-продажа завершена")
        return sale

    def generate_report(self) -> str:
        return "Отчет: онлайн-продажа"


class OfflineSaleProcess(SaleProcess):
    def sell_car(self, car: Car, customer: Customer):
        sale = super().sell_car(car, customer)
        self.log_action("Оффлайн-продажа завершена")
        return sale

    def generate_report(self) -> str:
        return "Отчет: оффлайн-продажа"