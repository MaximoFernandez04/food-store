"""
Dependencias compartidas de autenticación/autorización.

get_current_user valida el JWT y carga el usuario + sus roles.
require_role(["ADMIN", ...]) es la guard que usan los routers de TODOS los
módulos (no solo auth) para proteger endpoints por rol.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)


class CurrentUser:
    def __init__(self, usuario: Usuario, roles: list[str]):
        self.usuario = usuario
        self.roles = roles

    def has_role(self, *roles: str) -> bool:
        return any(role in self.roles for role in roles)


def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    usuario_id = int(payload["sub"])
    with UnitOfWork() as uow:
        usuario = uow.usuarios.get_by_id(usuario_id)
        if usuario is None or usuario.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
            )
        return CurrentUser(usuario=usuario, roles=payload.get("roles", []))


def require_role(allowed_roles: list[str]):
    def _check(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current.has_role(*allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requiere rol: {', '.join(allowed_roles)}",
            )
        return current

    return _check
