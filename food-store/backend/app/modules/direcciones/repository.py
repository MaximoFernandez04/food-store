from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.direcciones.model import DireccionEntrega


class DireccionRepository(BaseRepository[DireccionEntrega]):
    def __init__(self, session: Session):
        super().__init__(session, DireccionEntrega)

    def get_by_id(self, entity_id: int) -> Optional[DireccionEntrega]:
        d = self.session.get(DireccionEntrega, entity_id)
        if d and d.deleted_at is not None:
            return None
        return d

    def list_by_usuario(self, usuario_id: int) -> list[DireccionEntrega]:
        statement = select(DireccionEntrega).where(
            DireccionEntrega.usuario_id == usuario_id,
            DireccionEntrega.deleted_at.is_(None),
        )
        return list(self.session.exec(statement).all())

    def unset_principal(self, usuario_id: int) -> None:
        for direccion in self.list_by_usuario(usuario_id):
            if direccion.es_principal:
                direccion.es_principal = False
                self.session.add(direccion)
        self.session.flush()
