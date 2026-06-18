"""
Pago — registra cada intento de pago contra MercadoPago. Un Pedido puede
tener varios Pago (1:N) si el cliente reintenta tras un rechazo (RN-PA08).
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Pago(SQLModel, table=True):
    __tablename__ = "pago"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id", index=True)
    # ID que devuelve MercadoPago al crear el pago. NULL hasta que la
    # respuesta de la API llega.
    mp_payment_id: Optional[int] = Field(default=None, unique=True, index=True)
    mp_status: str = Field(max_length=30, default="pending")
    mp_status_detail: Optional[str] = Field(default=None, max_length=100)
    # UUID del Pedido (RN-PA09): vincula la preferencia/pago de MP con
    # nuestro pedido sin exponer el id secuencial.
    external_reference: str = Field(max_length=100, index=True)
    # RN-PA02: evita cobros duplicados por reintento de request. Generado
    # por el backend, único por intento de pago (no por pedido: un mismo
    # pedido puede tener varios intentos, cada uno con su propia key).
    idempotency_key: str = Field(max_length=100, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
