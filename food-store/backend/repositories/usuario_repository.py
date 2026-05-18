from sqlmodel import Session
from backend.models.usuario import Usuario
from typing import Optional, List

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, usuario: Usuario) -> None:
        self.session.add(usuario)

    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        return self.session.get(Usuario, user_id)

    def list(self) -> List[Usuario]:
        return self.session.query(Usuario).all()

    def remove(self, usuario: Usuario) -> None:
        self.session.delete(usuario)