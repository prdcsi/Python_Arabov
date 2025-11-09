from car import CAR_REGISTRY  # ←←← Импортируем глобальный реестр
from exceptions import InvalidCarError

class CarFactory:
    @staticmethod
    def create_car(car_type: str, **kwargs) -> 'Car':
        car_class = CAR_REGISTRY.get(car_type.lower())
        if not car_class:
            available = list(CAR_REGISTRY.keys())
            raise InvalidCarError(f"Неизвестный тип автомобиля: '{car_type}'. Доступны: {available}")
        return car_class(**kwargs)