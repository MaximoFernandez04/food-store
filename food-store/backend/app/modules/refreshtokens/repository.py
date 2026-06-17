from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.refreshtokens.model import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: Session):
        super().__init__(session, RefreshToken)

    def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
        return self.session.exec(statement).first()

    def revoke(self, token: RefreshToken) -> None:
        token.revoked_at = datetime.utcnow()
        self.update(token)

    def revoke_all_for_user(self, usuario_id: int) -> None:
        statement = select(RefreshToken).where(
            RefreshToken.usuario_id == usuario_id, RefreshToken.revoked_at.is_(None)
        )
        for token in self.session.exec(statement).all():
            token.revoked_at = datetime.utcnow()
            self.session.add(token)
        self.session.flush()
