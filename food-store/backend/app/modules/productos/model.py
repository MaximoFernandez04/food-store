"""
Dominio 2 — Catálogo de Productos (sección 3.2).
Producto, Ingrediente, ProductoCategoria (M:N + es_principal),
ProductoIngrediente (M:N + es_removible).
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = None
    # NUMERIC(10,2) — NUNCA float/double para dinero (RN-CA04). Usar Decimal
    # evita errores de redondeo de punto flotante en cálculos de totales.
    precio_base: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingrediente"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)
    es_alergeno: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None, index=True)


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    cat_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)


class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)
    es_removible: bool = Field(default=True)
