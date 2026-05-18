from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .item_orden import ItemOrden

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(..., nullable=False)
    precio: float = Field(..., nullable=False)
    stock: int = Field(default=0, nullable=False)

    items_orden: List["ItemOrden"] = Relationship(back_populates="producto")