"""
Lógica de negocio de autenticación. Stateless: nunca guarda estado entre
llamadas, todo entra por parámetro (uow, dto). Nunca hace
uow.session.commit() directamente — eso lo maneja el __exit__ del UoW.
"""
from app.core.exceptions import AppError
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.core.uow import UnitOfWork
from app.modules.auth.schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.modules.refreshtokens.model import RefreshToken
from app.modules.usuarios.model import Usuario

ROL_CLIENTE_DEFAULT = "CLIENT"


def register(uow: UnitOfWork, data: RegisterRequest) -> UserResponse:
    if uow.usuarios.get_by_email(data.email):
        raise AppError(
            status_code=400,
            detail="El email ya está registrado",
            code="EMAIL_TAKEN",
            field="email",
        )

    usuario = Usuario(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        telefono=data.telefono,
        password_hash=hash_password(data.password),
    )
    uow.usuarios.create(usuario)
    uow.usuarios.assign_role(usuario.id, ROL_CLIENTE_DEFAULT)

    return UserResponse(
        id=usuario.id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        roles=[ROL_CLIENTE_DEFAULT],
        created_at=usuario.created_at,
    )


def login(uow: UnitOfWork, data: LoginRequest) -> TokenResponse:
    usuario = uow.usuarios.get_by_email(data.email)
    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise AppError(
            status_code=401,
            detail="Credenciales inválidas",
            code="INVALID_CREDENTIALS",
        )

    roles = uow.usuarios.get_roles(usuario.id)
    return _issue_tokens(uow, usuario, roles)


def refresh(uow: UnitOfWork, refresh_token: str) -> TokenResponse | AppError:
    token_hash = hash_refresh_token(refresh_token)
    stored = uow.refresh_tokens.get_by_hash(token_hash)

    if not stored:
        raise AppError(
            status_code=401,
            detail="Refresh token inválido o expirado",
            code="INVALID_REFRESH_TOKEN",
        )

    if stored.revoked_at is not None:
        # RN-AU05: reuso de un refresh token ya utilizado = posible replay
        # attack. Mitigación: revocar TODOS los tokens activos del usuario.
        #
        # IMPORTANTE: devolvemos el AppError en vez de lanzarlo acá adentro.
        # Si lo lanzáramos dentro de este `with UnitOfWork()`, el __exit__
        # haría rollback() al ver la excepción — deshaciendo justo la
        # revocación de seguridad que queremos persistir. El router se
        # encarga de lanzarlo después de que el UoW haga commit.
        uow.refresh_tokens.revoke_all_for_user(stored.usuario_id)
        return AppError(
            status_code=401,
            detail="Refresh token ya utilizado. Por seguridad, todas las sesiones fueron cerradas.",
            code="REFRESH_TOKEN_REUSE_DETECTED",
        )

    if not stored.is_active:  # expirado naturalmente, no es reuso
        raise AppError(
            status_code=401,
            detail="Refresh token inválido o expirado",
            code="INVALID_REFRESH_TOKEN",
        )

    uow.refresh_tokens.revoke(stored)  # rotación: el viejo queda inválido

    usuario = uow.usuarios.get_by_id(stored.usuario_id)
    roles = uow.usuarios.get_roles(usuario.id)
    return _issue_tokens(uow, usuario, roles)


def logout(uow: UnitOfWork, refresh_token: str) -> None:
    token_hash = hash_refresh_token(refresh_token)
    stored = uow.refresh_tokens.get_by_hash(token_hash)
    if stored and stored.revoked_at is None:
        uow.refresh_tokens.revoke(stored)


def _issue_tokens(uow: UnitOfWork, usuario: Usuario, roles: list[str]) -> TokenResponse:
    from app.core.config import settings

    access_token = create_access_token(usuario.id, roles)
    raw_refresh, refresh_hash, expires_at = generate_refresh_token()

    uow.refresh_tokens.create(
        RefreshToken(
            usuario_id=usuario.id,
            token_hash=refresh_hash,
            expires_at=expires_at,
        )
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=raw_refresh,
        expires_in=settings.access_token_expire_minutes * 60,
    )
