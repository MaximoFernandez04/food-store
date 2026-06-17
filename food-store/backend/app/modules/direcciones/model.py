from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class DireccionEntrega(SQLModel, table=True):
    __tablename__ = "direccion_entrega"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    alias: Optional[str] = Field(default=None, max_length=50)
    linea1: str
    linea2: Optional[str] = None
    es_principal: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
