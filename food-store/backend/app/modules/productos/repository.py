from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.productos.model import (
    Ingrediente,
    Producto,
    ProductoCategoria,
    ProductoIngrediente,
)


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id(self, entity_id: int) -> Optional[Producto]:
        producto = self.session.get(Producto, entity_id)
        if producto and producto.deleted_at is not None:
            return None
        return producto

    def get_by_id_for_update(self, entity_id: int) -> Optional[Producto]:
        """Bloquea la fila (SELECT ... FOR UPDATE) para validar/descontar
        stock de forma segura ante condiciones de carrera (RN-PE04). En
        SQLite (usado en tests locales) with_for_update() es un no-op
        silencioso; en Postgres sí bloquea la fila hasta el commit/rollback
        de la transacción."""
        statement = (
            select(Producto)
            .where(Producto.id == entity_id, Producto.deleted_at.is_(None))
            .with_for_update()
        )
        return self.session.exec(statement).first()

    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        statement = select(Producto).where(
            Producto.nombre == nombre, Producto.deleted_at.is_(None)
        )
        return self.session.exec(statement).first()

    def search(
        self,
        categoria_id: Optional[int] = None,
        disponible: Optional[bool] = None,
        search: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Producto], int]:
        statement = select(Producto).where(Producto.deleted_at.is_(None))

        if categoria_id is not None:
            statement = statement.join(
                ProductoCategoria, ProductoCategoria.producto_id == Producto.id
            ).where(ProductoCategoria.cat_id == categoria_id)

        if disponible is not None:
            statement = statement.where(Producto.disponible == disponible)

        if search:
            statement = statement.where(Producto.nombre.ilike(f"%{search}%"))

        todos = list(self.session.exec(statement).all())
        total = len(todos)
        items = todos[(page - 1) * size : (page - 1) * size + size]
        return items, total

    def has_productos_activos(self, cat_id: int) -> bool:
        statement = (
            select(ProductoCategoria)
            .join(Producto, Producto.id == ProductoCategoria.producto_id)
            .where(ProductoCategoria.cat_id == cat_id, Producto.deleted_at.is_(None))
        )
        return self.session.exec(statement).first() is not None

    def asignar_categoria(self, producto_id: int, cat_id: int, es_principal: bool = False) -> None:
        self.session.add(
            ProductoCategoria(producto_id=producto_id, cat_id=cat_id, es_principal=es_principal)
        )
        self.session.flush()

    def asignar_ingrediente(self, producto_id: int, ingrediente_id: int, es_removible: bool = True) -> None:
        self.session.add(
            ProductoIngrediente(
                producto_id=producto_id, ingrediente_id=ingrediente_id, es_removible=es_removible
            )
        )
        self.session.flush()

    def quitar_ingrediente(self, producto_id: int, ingrediente_id: int) -> None:
        statement = select(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id,
            ProductoIngrediente.ingrediente_id == ingrediente_id,
        )
        rel = self.session.exec(statement).first()
        if rel:
            self.session.delete(rel)
            self.session.flush()

    def ingredientes_de(self, producto_id: int) -> list[Ingrediente]:
        statement = (
            select(Ingrediente)
            .join(ProductoIngrediente, ProductoIngrediente.ingrediente_id == Ingrediente.id)
            .where(ProductoIngrediente.producto_id == producto_id)
        )
        return list(self.session.exec(statement).all())


class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def get_by_id(self, entity_id: int) -> Optional[Ingrediente]:
        ingrediente = self.session.get(Ingrediente, entity_id)
        if ingrediente and ingrediente.deleted_at is not None:
            return None
        return ingrediente

    def get_by_nombre(self, nombre: str) -> Optional[Ingrediente]:
        statement = select(Ingrediente).where(Ingrediente.nombre == nombre)
        return self.session.exec(statement).first()
