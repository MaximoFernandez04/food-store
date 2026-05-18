from pydantic import BaseModel, Field
from datetime import datetime

class ProductoCreate(BaseModel):
    nombre: str = Field(..., description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto, debe ser mayor a 0")
    stock: int = Field(default=0, ge=0, description="Stock del producto, no puede ser negativo")

class ProductoUpdate(BaseModel):
    nombre: str = Field(None, description="Nombre del producto")
    precio: float = Field(None, gt=0, description="Precio del producto, debe ser mayor a 0")
    stock: int = Field(None, ge=0, description="Stock del producto, no puede ser negativo")

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True