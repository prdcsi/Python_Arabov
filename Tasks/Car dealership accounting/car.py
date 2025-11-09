from abc import ABC, ABCMeta, abstractmethod
from exceptions import InvalidCarError

# Глобальный реестр — вынесем его ВНЕ метакласса для ясности
CAR_REGISTRY = {}

class CarMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        # Регистрируем ВСЕ подклассы Car, кроме самого Car
        if name != "Car" and any(base.__name__ == "Car" for base in bases):
            CAR_REGISTRY[name.lower()] = cls
            print(f"[DEBUG] Зарегистрирован тип автомобиля: {name.lower()} → {cls}")
        return cls


class Car(ABC, metaclass=CarMeta):
    def __init__(self, car_id: str, make: str, model: str, year: int, price: float):
        if not (1900 <= year <= 2030):
            raise InvalidCarError("Некорректный год выпуска")
        if price <= 0:
            raise InvalidCarError("Цена должна быть положительной")
        self._car_id = car_id
        self._make = make
        self._model = model
        self._year = year
        self._price = price
        self._is_available = True

    @property
    def car_id(self) -> str:
        return self._car_id

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model

    @property
    def year(self) -> int:
        return self._year

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise InvalidCarError("Цена должна быть положительной")
        self._price = value

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, value: bool):
        self._is_available = value

    @abstractmethod
    def calculate_price(self) -> float:
        pass

    def __str__(self) -> str:
        return f"Автомобиль: {self.make} {self.model}, Год выпуска: {self.year}"

    def __eq__(self, other):
        if isinstance(other, Car):
            return self.car_id == other.car_id
        return False

    def __lt__(self, other):
        if isinstance(other, Car):
            return self.price < other.price
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Car):
            return self.price > other.price
        return NotImplemented

    def to_dict(self) -> dict:
        return {
            "car_id": self.car_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "is_available": self.is_available,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls,  dict):
        car_type = data.pop("type")
        car_class = CAR_REGISTRY[car_type.lower()]
        return car_class(**data)


class Sedan(Car):
    def __init__(self, car_id: str, make: str, model: str, year: int, price: float, fuel_efficiency: float):
        super().__init__(car_id, make, model, year, price)
        self._fuel_efficiency = fuel_efficiency

    @property
    def fuel_efficiency(self) -> float:
        return self._fuel_efficiency

    def calculate_price(self) -> float:
        return self.price * 0.95

    def __str__(self) -> str:
        return f"Седан: {self.make} {self.model}, Расход топлива: {self.fuel_efficiency} л/100км"


class SUV(Car):
    def __init__(self, car_id: str, make: str, model: str, year: int, price: float, towing_capacity: float):
        super().__init__(car_id, make, model, year, price)
        self._towing_capacity = towing_capacity

    @property
    def towing_capacity(self) -> float:
        return self._towing_capacity

    def calculate_price(self) -> float:
        return self.price * 1.1

    def __str__(self) -> str:
        return f"SUV: {self.make} {self.model}, Грузоподъемность: {self.towing_capacity} кг"


class ElectricCar(Car):
    def __init__(self, car_id: str, make: str, model: str, year: int, price: float, battery_range: float):
        super().__init__(car_id, make, model, year, price)
        self._battery_range = battery_range

    @property
    def battery_range(self) -> float:
        return self._battery_range

    def calculate_price(self) -> float:
        return self.price * 0.9

    def __str__(self) -> str:
        return f"Электромобиль: {self.make} {self.model}, Запас хода: {self.battery_range} км"