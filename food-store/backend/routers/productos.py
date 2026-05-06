from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas import ProductoResponse
from backend.models import Producto
from backend.database import get_db

router = APIRouter()

@router.get("/productos", response_model=list[ProductoResponse])
def list_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos