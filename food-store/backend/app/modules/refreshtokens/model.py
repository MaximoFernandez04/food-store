"""
RefreshToken — permite invalidar sesiones en logout (revoked_at) y validar
expiración server-side. Nunca se guarda el token en texto plano: se guarda
el hash SHA-256 (token_hash), tal como pide la spec.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.modules.usuarios.model import Usuario


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_token"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    token_hash: str = Field(max_length=64, unique=True, index=True)
    expires_at: datetime
    revoked_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    usuario: Optional[Usuario] = Relationship(back_populates="refresh_tokens")

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > datetime.utcnow()
