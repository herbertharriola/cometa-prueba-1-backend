from fastapi import APIRouter
from app.services.stock_service import get_beers

router = APIRouter()

@router.get("/beers")
def list_beers():
    return get_beers()
