from car import CarMeta
from exceptions import InvalidCarError

class CarFactory:
    @staticmethod
    def create_car(car_type: str, **kwargs) -> Car:
        car_class = CarMeta.registry.get(car_type.lower())
        if not car_class:
            raise InvalidCarError(f"Неизвестный тип автомобиля: {car_type}")
        return car_class(**kwargs)