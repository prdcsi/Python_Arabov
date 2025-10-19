class InvalidCarError(Exception):
    """Исключение для некорректных данных автомобиля."""
    pass


class PermissionDeniedError(Exception):
    """Исключение при отсутствии прав доступа."""
    pass


class SaleNotFoundError(Exception):
    """Исключение, если продажа не найдена."""
    pass