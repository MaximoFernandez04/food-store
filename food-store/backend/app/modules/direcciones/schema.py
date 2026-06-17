from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DireccionCreate(BaseModel):
    alias: Optional[str] = Field(default=None, max_length=50)
    linea1: str = Field(min_length=3)
    linea2: Optional[str] = None
    es_principal: bool = False


class DireccionUpdate(BaseModel):
    alias: Optional[str] = Field(default=None, max_length=50)
    linea1: Optional[str] = Field(default=None, min_length=3)
    linea2: Optional[str] = None


class DireccionRead(BaseModel):
    id: int
    alias: Optional[str]
    linea1: str
    linea2: Optional[str]
    es_principal: bool
    created_at: datetime

    class Config:
        from_attributes = True
