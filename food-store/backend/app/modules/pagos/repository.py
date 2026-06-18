from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.pagos.model import Pago


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session: Session):
        super().__init__(session, Pago)

    def get_by_idempotency_key(self, idempotency_key: str) -> Optional[Pago]:
        statement = select(Pago).where(Pago.idempotency_key == idempotency_key)
        return self.session.exec(statement).first()

    def get_by_mp_payment_id(self, mp_payment_id: int) -> Optional[Pago]:
        statement = select(Pago).where(Pago.mp_payment_id == mp_payment_id)
        return self.session.exec(statement).first()

    def list_by_pedido(self, pedido_id: int) -> list[Pago]:
        statement = (
            select(Pago)
            .where(Pago.pedido_id == pedido_id)
            .order_by(Pago.created_at.desc())
        )
        return list(self.session.exec(statement).all())

    def get_ultimo_de_pedido(self, pedido_id: int) -> Optional[Pago]:
        pagos = self.list_by_pedido(pedido_id)
        return pagos[0] if pagos else None
