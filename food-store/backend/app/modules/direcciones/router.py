from fastapi import APIRouter, Depends, status

from app.core.deps import CurrentUser, get_current_user
from app.core.uow import UnitOfWork
from app.modules.direcciones import service
from app.modules.direcciones.schema import DireccionCreate, DireccionRead, DireccionUpdate

router = APIRouter(prefix="/api/v1/direcciones", tags=["direcciones"])


@router.get("", response_model=list[DireccionRead])
def list_mis_direcciones(current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        return uow.direcciones.list_by_usuario(current.usuario.id)


@router.post("", response_model=DireccionRead, status_code=status.HTTP_201_CREATED)
def create_direccion(
    data: DireccionCreate, current: CurrentUser = Depends(get_current_user)
):
    with UnitOfWork() as uow:
        return service.create_direccion(uow, current.usuario.id, data)


@router.put("/{direccion_id}", response_model=DireccionRead)
def update_direccion(
    direccion_id: int,
    data: DireccionUpdate,
    current: CurrentUser = Depends(get_current_user),
):
    with UnitOfWork() as uow:
        return service.update_direccion(uow, current.usuario.id, direccion_id, data)


@router.patch("/{direccion_id}/principal", response_model=DireccionRead)
def set_principal(direccion_id: int, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        return service.set_principal(uow, current.usuario.id, direccion_id)


@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_direccion(direccion_id: int, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        service.delete_direccion(uow, current.usuario.id, direccion_id)
