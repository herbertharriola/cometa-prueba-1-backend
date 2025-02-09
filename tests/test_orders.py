import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.order_service import orders

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_orders():
    """Limpia las órdenes antes de cada prueba para asegurar independencia."""
    orders.clear()


def test_list_orders():
    """Prueba que la lista de órdenes se obtenga correctamente."""
    response = client.get("/orders")
    assert response.status_code == 200
    assert "orders" in response.json()
    assert isinstance(response.json()["orders"], list)


def test_create_order():
    """Prueba la creación de una nueva orden."""
    order_data = {
        "items": [  # ⬅ La lista ahora está envuelta en un objeto
            {"name": "Corona", "quantity": 2, "price_per_unit": 115.0}
        ]
    }
    response = client.post("/order", json=order_data)
    assert response.status_code == 200, response.text  # ⬅ Muestra más detalles en caso de error


def test_get_order_status():
    """Prueba la obtención del estado de una orden existente."""
    test_create_order()  # Crear una orden primero
    response = client.get("/order/0")  # Consultar la primera orden
    assert response.status_code == 200
    assert "created" in response.json()
    assert "subtotal" in response.json()
    assert "items" in response.json()


def test_update_order():
    """Prueba actualizar una orden existente."""
    test_create_order()  # Crear una orden antes de actualizar

    # Modificar el stock para evitar error de stock insuficiente
    from app.services.stock_service import stock_data
    stock_data["beers"][0]["quantity"] = 10  # Asegurar stock de "Corona"

    update_data = [
        {"name": "Corona", "quantity": 1, "price_per_unit": 115}
    ]
    response = client.put("/order/0", json=update_data)
    assert response.status_code == 200, response.text  # Se añade response.text para ver el mensaje de error
    json_response = response.json()
    assert json_response["message"] == "Orden actualizada"
    assert "order_details" in json_response



def test_order_insufficient_stock():
    """Prueba crear una orden con cantidad mayor al stock disponible."""
    order_data = {
        "items": [
            {"name": "Corona", "quantity": 20, "price_per_unit": 115}  # Excediendo stock
        ]
    }
    response = client.post("/order", json=order_data)
    assert response.status_code == 400
    assert "No hay suficiente stock de Corona" in response.json()["detail"]


def test_update_invalid_order():
    """Prueba actualizar una orden inexistente."""
    update_data = [
        {"name": "Corona", "quantity": 1, "price_per_unit": 115}
    ]
    response = client.put("/order/999", json=update_data)  # ID inexistente
    assert response.status_code == 404, response.text
    assert response.json()["detail"] in ["Orden no encontrada", "Not Found"]


def test_get_beers():
    """Prueba obtener la lista de cervezas disponibles."""
    response = client.get("/beers")
    assert response.status_code == 200
    json_response = response.json()
    assert "beers" in json_response
    assert isinstance(json_response["beers"], list)
    assert len(json_response["beers"]) > 0  # Debe haber al menos una cerveza
