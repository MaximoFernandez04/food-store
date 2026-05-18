from typing import List, Optional
from sqlmodel import select, Session
from backend.models.producto import Producto

class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, producto: Producto) -> None:
        self.session.add(producto)

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.session.get(Producto, producto_id)

    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        statement = select(Producto).where(Producto.nombre == nombre)
        return self.session.exec(statement).first()

    def list(self) -> List[Producto]:
        statement = select(Producto)
        return self.session.exec(statement).all()

    def delete(self, producto: Producto) -> None:
        self.session.delete(producto)