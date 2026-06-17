from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.usuarios.model import Usuario, UsuarioRol


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        statement = select(Usuario).where(
            Usuario.email == email, Usuario.deleted_at.is_(None)
        )
        return self.session.exec(statement).first()

    def get_roles(self, usuario_id: int) -> list[str]:
        statement = select(UsuarioRol.rol_codigo).where(
            UsuarioRol.usuario_id == usuario_id
        )
        return list(self.session.exec(statement).all())

    def assign_role(self, usuario_id: int, rol_codigo: str) -> None:
        self.session.add(
            UsuarioRol(usuario_id=usuario_id, rol_codigo=rol_codigo)
        )
        self.session.flush()
