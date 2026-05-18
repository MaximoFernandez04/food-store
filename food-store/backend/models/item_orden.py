from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .orden import Orden
from .producto import Producto

class ItemOrden(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: Optional[int] = Field(default=None, foreign_key="orden.id")
    producto_id: Optional[int] = Field(default=None, foreign_key="producto.id")
    cantidad: int = Field(..., nullable=False)
    precio_unitario: float = Field(..., nullable=False)

    orden: Optional[Orden] = Relationship(back_populates="items")
    producto: Optional[Producto] = Relationship(back_populates="items_orden")