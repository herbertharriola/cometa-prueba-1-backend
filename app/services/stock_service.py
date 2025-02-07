stock_data = {
    "last_updated": "2024-09-10 12:00:00",
    "beers": [
        {"name": "Corona", "price": 115, "quantity": 5},
        {"name": "Quilmes", "price": 120, "quantity": 2},
        {"name": "Club Colombia", "price": 110, "quantity": 10}
    ]
}

def get_stock():
    return stock_data

def get_beers():
    return {"last_updated": stock_data["last_updated"], "beers": stock_data["beers"]}
