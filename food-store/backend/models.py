from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(..., nullable=False)
    email: str = Field(..., index=True, nullable=False, unique=True)

    ordenes: List["Orden"] = Relationship(back_populates="usuario")

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(..., nullable=False)
    precio: float = Field(..., nullable=False)
    stock: int = Field(default=0, nullable=False)

    items_orden: List["ItemOrden"] = Relationship(back_populates="producto")

class Orden(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    usuario: Optional[Usuario] = Relationship(back_populates="ordenes")
    items: List["ItemOrden"] = Relationship(back_populates="orden")

class ItemOrden(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: Optional[int] = Field(default=None, foreign_key="orden.id")
    producto_id: Optional[int] = Field(default=None, foreign_key="producto.id")
    cantidad: int = Field(..., nullable=False)
    precio_unitario: float = Field(..., nullable=False)

    orden: Optional[Orden] = Relationship(back_populates="items")
    producto: Optional[Producto] = Relationship(back_populates="items_orden")