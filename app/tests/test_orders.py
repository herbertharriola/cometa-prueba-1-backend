from fastapi import APIRouter
from app.services.order_service import create_order, get_order_status
from typing import List, Dict

router = APIRouter()

@router.post("/order")
def new_order(items: List[Dict]):
    return create_order(items)

@router.get("/order/{order_id}")
def order_status(order_id: int):
    return get_order_status(order_id)
