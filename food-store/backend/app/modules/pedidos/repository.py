from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.pedidos.model import (
    DetallePedido,
    EstadoPedido,
    FormaPago,
    HistorialEstadoPedido,
    Pedido,
)


class EstadoPedidoRepository(BaseRepository[EstadoPedido]):
    def __init__(self, session: Session):
        super().__init__(session, EstadoPedido)


class FormaPagoRepository(BaseRepository[FormaPago]):
    def __init__(self, session: Session):
        super().__init__(session, FormaPago)


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def get_by_id_for_update(self, pedido_id: int) -> Optional[Pedido]:
        statement = select(Pedido).where(Pedido.id == pedido_id).with_for_update()
        return self.session.exec(statement).first()

    def get_by_external_ref(self, external_ref) -> Optional[Pedido]:
        statement = select(Pedido).where(Pedido.external_ref == external_ref)
        return self.session.exec(statement).first()

    def search(
        self,
        usuario_id: Optional[int] = None,
        estado: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Pedido], int]:
        statement = select(Pedido)
        if usuario_id is not None:
            statement = statement.where(Pedido.usuario_id == usuario_id)
        if estado is not None:
            statement = statement.where(Pedido.estado_codigo == estado)
        statement = statement.order_by(Pedido.created_at.desc())

        todos = list(self.session.exec(statement).all())
        total = len(todos)
        items = todos[(page - 1) * size : (page - 1) * size + size]
        return items, total


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(session, DetallePedido)

    def list_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        statement = select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        return list(self.session.exec(statement).all())


class HistorialRepository(BaseRepository[HistorialEstadoPedido]):
    def __init__(self, session: Session):
        super().__init__(session, HistorialEstadoPedido)

    def list_by_pedido(self, pedido_id: int) -> list[HistorialEstadoPedido]:
        statement = (
            select(HistorialEstadoPedido)
            .where(HistorialEstadoPedido.pedido_id == pedido_id)
            .order_by(HistorialEstadoPedido.created_at.asc())
        )
        return list(self.session.exec(statement).all())
