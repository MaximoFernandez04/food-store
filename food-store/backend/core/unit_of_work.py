from sqlmodel import Session
from backend.repositories import (
    UsuarioRepository,
    ProductoRepository,
    OrdenRepository,
    ItemOrdenRepository
)
from backend.core.database import engine

class UnitOfWork:
    def __init__(self):
        self.session = Session(engine)
        self.usuario_repository = UsuarioRepository(self.session)
        self.producto_repository = ProductoRepository(self.session)
        self.orden_repository = OrdenRepository(self.session)
        self.item_orden_repository = ItemOrdenRepository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()