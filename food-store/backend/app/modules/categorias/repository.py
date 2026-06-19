from typing import Optional

from sqlmodel import Session, select, text

from app.core.base_repository import BaseRepository
from app.modules.categorias.model import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_by_id(self, entity_id: int) -> Optional[Categoria]:
        cat = self.session.get(Categoria, entity_id)
        if cat and cat.deleted_at is not None:
            return None
        return cat

    def list_raiz(self) -> list[Categoria]:
        statement = select(Categoria).where(
            Categoria.parent_id.is_(None), Categoria.deleted_at.is_(None)
        )
        return list(self.session.exec(statement).all())

    def list_activas(self) -> list[Categoria]:
        """A diferencia de BaseRepository.list_all() (genérico, sin
        filtros), esta sí respeta soft-delete — es la que debe usar
        cualquier GET de listado (sección 5: 'todos los GET filtran
        WHERE deleted_at IS NULL')."""
        statement = select(Categoria).where(Categoria.deleted_at.is_(None)).order_by(Categoria.nombre)
        return list(self.session.exec(statement).all())

    def list_hijos(self, parent_id: int) -> list[Categoria]:
        statement = select(Categoria).where(
            Categoria.parent_id == parent_id, Categoria.deleted_at.is_(None)
        )
        return list(self.session.exec(statement).all())

    def has_hijos_activos(self, categoria_id: int) -> bool:
        return len(self.list_hijos(categoria_id)) > 0

    def arbol_completo(self) -> list[dict]:
        """CTE recursiva: devuelve todas las categorías activas con su
        profundidad (depth) en el árbol, ordenadas para reconstruir la
        jerarquía fácilmente en el frontend."""
        query = text(
            """
            WITH RECURSIVE categoria_tree AS (
                SELECT id, nombre, parent_id, 0 AS depth
                FROM categoria
                WHERE parent_id IS NULL AND deleted_at IS NULL
                UNION ALL
                SELECT c.id, c.nombre, c.parent_id, ct.depth + 1
                FROM categoria c
                JOIN categoria_tree ct ON c.parent_id = ct.id
                WHERE c.deleted_at IS NULL
            )
            SELECT id, nombre, parent_id, depth FROM categoria_tree
            ORDER BY depth, nombre
            """
        )
        result = self.session.exec(query)  # type: ignore[arg-type]
        return [dict(row._mapping) for row in result]
