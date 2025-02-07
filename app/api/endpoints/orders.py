from fastapi import APIRouter
from app.services.order_service import create_order, get_order_status, update_order, get_orders
from app.models.order import OrderItem
from typing import List

router = APIRouter()

@router.get("/orders")
def list_orders():
    return get_orders()

@router.post("/order")
def new_order(items: List[OrderItem]):
    return create_order(items)

@router.get("/order/{order_id}")
def order_status(order_id: int):
    return get_order_status(order_id)

@router.put("/order/{order_id}")
def modify_order(order_id: int, new_items: List[OrderItem]):
    return update_order(order_id, new_items)
