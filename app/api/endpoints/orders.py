from fastapi import APIRouter
from pydantic import BaseModel
from app.services.order_service import create_order, get_order_status, get_orders, update_order
from app.models.order import OrderItem
from typing import List

router = APIRouter()

class OrderRequest(BaseModel):
    items: List[OrderItem]

@router.get("/orders")
def list_orders():
    return get_orders()

@router.post("/order")
def new_order(order: OrderRequest):  # ⬅ Cambio en la firma
    return create_order(order.items)

@router.get("/order/{order_id}")
def order_status(order_id: int):
    return get_order_status(order_id)

@router.put("/order/{order_id}")
def modify_order(order_id: int, new_items: List[OrderItem]):
    return update_order(order_id, new_items)
