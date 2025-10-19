from abc import ABC, abstractmethod

class Sellable(ABC):
    @abstractmethod
    def sell_car(self, car, customer):
        pass


class Reportable(ABC):
    @abstractmethod
    def generate_report(self):
        pass