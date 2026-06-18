from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CrearPagoRequest(BaseModel):
    pedido_id: int
    token: str  # card_token generado por MercadoPago.js en el navegador
    payer_email: EmailStr
    installments: int = 1


class PagoResponse(BaseModel):
    id: int
    pedido_id: int
    mp_payment_id: Optional[int]
    mp_status: str
    mp_status_detail: Optional[str]
    external_reference: str
    created_at: datetime

    class Config:
        from_attributes = True
