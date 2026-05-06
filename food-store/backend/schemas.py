from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# Schemas para Producto
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int

    class Config:
        from_attributes = True

# Schemas para Orden
class ItemOrdenCreate(BaseModel):
    producto_id: int
    cantidad: int

class OrdenCreate(BaseModel):
    usuario_id: int
    items: List[ItemOrdenCreate]

class OrdenResponse(BaseModel):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True