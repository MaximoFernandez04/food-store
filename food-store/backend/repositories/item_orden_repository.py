from sqlmodel import Session
from typing import Optional, List
from backend.models.item_orden import ItemOrden

class ItemOrdenRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, item_orden: ItemOrden) -> None:
        self.session.add(item_orden)

    def list_by_orden_id(self, orden_id: int) -> List[ItemOrden]:
        return self.session.query(ItemOrden).filter(ItemOrden.orden_id == orden_id).all()

    def delete(self, item_orden: ItemOrden) -> None:
        self.session.delete(item_orden)