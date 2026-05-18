from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .usuario import Usuario
from .item_orden import ItemOrden

class Orden(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    estado: str = Field(default="PENDIENTE", nullable=False)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    usuario: Optional[Usuario] = Relationship(back_populates="ordenes")
    items: List["ItemOrden"] = Relationship(back_populates="orden")