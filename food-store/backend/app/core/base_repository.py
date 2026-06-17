"""
BaseRepository[T] genérico — sección 7.2 de la especificación.

Cada repositorio concreto (UsuarioRepository, ProductoRepository, etc.)
hereda de esta clase para no reescribir get_by_id / list_all / create /
soft_delete en cada módulo. Las queries específicas de cada dominio van
en el repositorio concreto, no acá.
"""
from datetime import datetime, timezone
from typing import Generic, Optional, Type, TypeVar

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.session.get(self.model, entity_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def count(self) -> int:
        statement = select(self.model)
        return len(list(self.session.exec(statement).all()))

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def soft_delete(self, entity: T) -> None:
        if not hasattr(entity, "deleted_at"):
            raise AttributeError(
                f"{self.model.__name__} no tiene campo deleted_at; "
                "usá hard_delete o agregá soft-delete al modelo."
            )
        setattr(entity, "deleted_at", datetime.now(timezone.utc))
        self.session.add(entity)
        self.session.flush()

    def hard_delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.flush()
