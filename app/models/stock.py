from pydantic import BaseModel

class Stock(BaseModel):
    name: str
    price: float
    quantity: int