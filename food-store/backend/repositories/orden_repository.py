from sqlmodel import Session, select
from typing import Optional, List
from backend.models.orden import Orden

class OrdenRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, orden: Orden) -> None:
        self.session.add(orden)

    def get_by_id(self, orden_id: int) -> Optional[Orden]:
        return self.session.get(Orden, orden_id)

    def list_by_usuario(self, usuario_id: int) -> List[Orden]:
        statement = select(Orden).where(Orden.usuario_id == usuario_id)
        return self.session.exec(statement).all()

    def list_all(self) -> List[Orden]:
        statement = select(Orden)
        return self.session.exec(statement).all()