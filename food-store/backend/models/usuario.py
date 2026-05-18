from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .orden import Orden

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(..., nullable=False)
    email: str = Field(..., index=True, nullable=False, unique=True)
    password_hash: str
    role: str = Field(..., nullable=False)

    ordenes: List["Orden"] = Relationship(back_populates="usuario")