from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.modules.categorias.schema import CategoriaRead


class IngredienteCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    es_alergeno: bool = False


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    es_alergeno: bool

    class Config:
        from_attributes = True


class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_cantidad: int = Field(default=0, ge=0)
    categoria_ids: list[int] = Field(default_factory=list)
    ingrediente_ids: list[int] = Field(default_factory=list)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[Decimal] = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None
    # Si se manda, REEMPLAZA por completo el set de categorías/ingredientes
    # asociados (no es un merge incremental) — más simple para el form de
    # edición del admin, que siempre manda la lista completa actual.
    categoria_ids: Optional[list[int]] = None
    ingrediente_ids: Optional[list[int]] = None


class DisponibilidadUpdate(BaseModel):
    disponible: bool


class StockUpdate(BaseModel):
    stock_cantidad: int = Field(ge=0)


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio_base: Decimal
    stock_cantidad: int
    disponible: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductoDetail(ProductoRead):
    ingredientes: list[IngredienteRead] = Field(default_factory=list)
    categorias: list[CategoriaRead] = Field(default_factory=list)


class PaginatedProductos(BaseModel):
    items: list[ProductoRead]
    total: int
    page: int
    size: int
