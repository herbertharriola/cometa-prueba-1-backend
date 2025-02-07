from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class OrderItem(BaseModel):
    name: str
    quantity: int
    price_per_unit: float
    total: float = Field(default=0)

    @classmethod
    def calculate_total(cls, price_per_unit: float, quantity: int) -> float:
        return round(price_per_unit * quantity, 2)

    def __init__(self, **data):
        super().__init__(**data)
        self.total = self.calculate_total(self.price_per_unit, self.quantity)

class Order(BaseModel):
    created: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    paid: bool = False
    subtotal: float = 0
    taxes: float = 0
    discounts: float = 0
    total: float = 0
    items: List[OrderItem] = []
    rounds: List[List[OrderItem]] = []