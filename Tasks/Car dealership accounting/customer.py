class Customer:
    def __init__(self, customer_id: str, name: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone

    def __str__(self) -> str:
        return f"Клиент: {self.name} (ID: {self.customer_id})"

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)