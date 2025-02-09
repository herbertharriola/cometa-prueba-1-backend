import random
from app.models.order import Order, OrderItem
from app.services.stock_service import stock_data
from fastapi import HTTPException
from typing import List, Dict

orders = []

def get_orders():
    return {"orders": [order.model_dump() for order in orders]}

def calculate_order_total(order: Order):
    subtotal = sum(item.total for item in order.items)
    taxes = subtotal * 0.12  # 12% impuesto
    total = subtotal + taxes - order.discounts
    return subtotal, taxes, total

def create_order(items: List[OrderItem]):
    order = Order()
    for item in items:
        if not isinstance(item, dict):
            item = item.dict()  # Asegurar que los datos sean un diccionario
        beer = next((b for b in stock_data['beers'] if b["name"] == item["name"]), None)
        if not beer or beer["quantity"] < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"No hay suficiente stock de {item['name']}")
        beer["quantity"] -= item["quantity"]
        order_item = OrderItem(name=item["name"], price_per_unit=beer["price"], quantity=item["quantity"])
        order.items.append(order_item)
    order.subtotal, order.taxes, order.total = calculate_order_total(order)
    order.rounds.append(order.items.copy())
    orders.append(order)
    return {"order_id": len(orders) - 1, "details": order.model_dump()}

def get_order_status(order_id: int):
    if order_id >= len(orders) or order_id < 0:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orders[order_id].model_dump()

def update_order(order_id: int, new_items: List[OrderItem]):
    if order_id >= len(orders) or order_id < 0:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    order = orders[order_id]
    round_items = []

    for item in new_items:
        if not isinstance(item, dict):
            item = item.dict()  # Asegurar que los datos sean un diccionario

        beer = next((b for b in stock_data['beers'] if b["name"] == item["name"]), None)
        if not beer or beer["quantity"] < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"No hay suficiente stock de {item['name']}")
        
        beer["quantity"] -= item["quantity"]

        # Aplicar descuento aleatorio entre 0% y 25%
        discount_rate = random.choice([0, 5, 10, 15, 20, 25, 30])/100
        discounted_price = round(beer["price"] * (1 - discount_rate), 2)
        discount_amount = round(beer["price"] * discount_rate * item["quantity"], 2)

        # Se agrega el item con precio original al listado de items
        order_item = OrderItem(name=item["name"], price_per_unit=beer["price"], quantity=item["quantity"])
        order.items.append(order_item)

        # Se agrega el item con descuento al listado que se insertará en el listado de rondas
        discounted_item = OrderItem(name=item["name"], price_per_unit=discounted_price, quantity=item["quantity"])
        round_items.append(discounted_item)

        # Acumular el descuento total en `order.discounts`
        order.discounts += discount_amount
    order.subtotal, order.taxes, order.total = calculate_order_total(order)
    order.rounds.append(round_items)
    return {"message": "Orden actualizada", "order_details": order.model_dump()}
