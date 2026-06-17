from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ItemPedidoRequest(BaseModel):
    producto_id: int
    cantidad: int = Field(ge=1)
    personalizacion: Optional[list[int]] = None


class CrearPedidoRequest(BaseModel):
    items: list[ItemPedidoRequest] = Field(min_length=1)
    forma_pago_codigo: str
    direccion_id: Optional[int] = None  # None = retiro en local
    notas: Optional[str] = None


class AvanzarEstadoRequest(BaseModel):
    nuevo_estado: str
    motivo: Optional[str] = None


class DetallePedidoRead(BaseModel):
    id: int
    producto_id: int
    nombre_snapshot: str
    precio_snapshot: Decimal
    cantidad: int
    subtotal: Decimal
    personalizacion: Optional[list[int]]

    class Config:
        from_attributes = True


class HistorialRead(BaseModel):
    id: int
    estado_desde: Optional[str]
    estado_hasta: str
    usuario_id: Optional[int]
    motivo: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PedidoRead(BaseModel):
    id: int
    estado_codigo: str
    subtotal: Decimal
    costo_envio: Decimal
    total: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class PedidoDetail(PedidoRead):
    forma_pago_codigo: str
    direccion_id: Optional[int]
    notas: Optional[str]
    items: list[DetallePedidoRead] = Field(default_factory=list)
    historial: list[HistorialRead] = Field(default_factory=list)


class PaginatedPedidos(BaseModel):
    items: list[PedidoRead]
    total: int
    page: int
    size: int
