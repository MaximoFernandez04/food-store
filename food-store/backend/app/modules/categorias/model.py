"""
Categoria: jerarquía recursiva (self-FK), ON DELETE SET NULL en parent_id.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    parent_id: Optional[int] = Field(
        default=None, foreign_key="categoria.id", nullable=True
    )
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
