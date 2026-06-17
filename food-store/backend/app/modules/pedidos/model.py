"""
Dominio 3 — Ventas, Pagos y Trazabilidad (sección 3.3).
EstadoPedido y FormaPago son catálogos. Pedido es el agregado central.
DetallePedido aplica snapshot (nombre/precio inmutables). HistorialEstadoPedido
es append-only: ninguna capa superior emite UPDATE/DELETE sobre esta tabla.

FormaPago se define acá (no en productos/) porque solo lo usa Pedido y así
se evita una dependencia cruzada entre productos y pedidos sin necesidad.
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import ARRAY, Column, Integer
from sqlmodel import Field, SQLModel


class EstadoPedido(SQLModel, table=True):
    __tablename__ = "estado_pedido"

    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: Optional[str] = None
    orden: int
    es_terminal: bool = Field(default=False)


class FormaPago(SQLModel, table=True):
    __tablename__ = "forma_pago"

    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: Optional[str] = None
    habilitado: bool = Field(default=True)


class Pedido(SQLModel, table=True):
    __tablename__ = "pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    estado_codigo: str = Field(foreign_key="estado_pedido.codigo", index=True)
    forma_pago_codigo: str = Field(foreign_key="forma_pago.codigo")
    direccion_id: Optional[int] = Field(default=None, foreign_key="direccion_entrega.id")
    # Snapshot de texto de la dirección al momento de crear el pedido (RN-DA06):
    # si el usuario edita o borra la dirección después, el pedido histórico no
    # se ve afectado. NULL = retiro en local.
    direccion_texto_snapshot: Optional[str] = None
    subtotal: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    costo_envio: Decimal = Field(default=Decimal("50.00"), max_digits=10, decimal_places=2)
    total: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    notas: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalle_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id", index=True)
    producto_id: int = Field(foreign_key="producto.id")
    # Snapshot (RN-PE02): nombre y precio inmutables aunque el producto
    # cambie o se borre después.
    nombre_snapshot: str = Field(max_length=200)
    precio_snapshot: Decimal = Field(max_digits=10, decimal_places=2)
    cantidad: int = Field(ge=1)
    subtotal: Decimal = Field(max_digits=10, decimal_places=2)
    # RN-PE07: array de PostgreSQL con los IDs de ingredientes excluidos.
    personalizacion: Optional[list[int]] = Field(
        default=None, sa_column=Column(ARRAY(Integer), nullable=True)
    )


class HistorialEstadoPedido(SQLModel, table=True):
    __tablename__ = "historial_estado_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id", index=True)
    estado_desde: Optional[str] = Field(default=None, foreign_key="estado_pedido.codigo")
    estado_hasta: str = Field(foreign_key="estado_pedido.codigo")
    # NULL = transición ejecutada por el Sistema (ej: webhook de pago), no
    # por un usuario humano.
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    motivo: Optional[str] = None
    # Append-only (RN-03/RN-FS07): esta tabla NUNCA recibe UPDATE ni DELETE
    # desde ninguna capa. Por eso no tiene updated_at.
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
