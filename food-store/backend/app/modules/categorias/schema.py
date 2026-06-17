from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    parent_id: Optional[int] = None


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    parent_id: Optional[int] = None


class CategoriaRead(BaseModel):
    id: int
    nombre: str
    parent_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class CategoriaArbolNode(BaseModel):
    id: int
    nombre: str
    parent_id: Optional[int]
    depth: int
