"""
Router puro: parsea, delega al service, serializa. Sin lógica de negocio.
"""
from fastapi import APIRouter, Request, status

from app.core.deps import get_current_user, CurrentUser
from app.core.exceptions import AppError
from app.core.rate_limit import limiter
from app.core.uow import UnitOfWork
from app.modules.auth import service
from app.modules.auth.schema import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from fastapi import Depends

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_endpoint(data: RegisterRequest):
    with UnitOfWork() as uow:
        return service.register(uow, data)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/15minutes")
def login_endpoint(request: Request, data: LoginRequest):
    with UnitOfWork() as uow:
        return service.login(uow, data)


@router.post("/refresh", response_model=TokenResponse)
def refresh_endpoint(data: RefreshRequest):
    with UnitOfWork() as uow:
        result = service.refresh(uow, data.refresh_token)
    if isinstance(result, AppError):
        raise result
    return result


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_endpoint(data: LogoutRequest):
    with UnitOfWork() as uow:
        service.logout(uow, data.refresh_token)


@router.get("/me", response_model=UserResponse)
def me_endpoint(current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        roles = uow.usuarios.get_roles(current.usuario.id)
    return UserResponse(
        id=current.usuario.id,
        nombre=current.usuario.nombre,
        apellido=current.usuario.apellido,
        email=current.usuario.email,
        telefono=current.usuario.telefono,
        roles=roles,
        created_at=current.usuario.created_at,
    )
