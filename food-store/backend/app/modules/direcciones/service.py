from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.direcciones.model import DireccionEntrega
from app.modules.direcciones.schema import DireccionCreate, DireccionUpdate


def create_direccion(uow: UnitOfWork, usuario_id: int, data: DireccionCreate) -> DireccionEntrega:
    es_primera = len(uow.direcciones.list_by_usuario(usuario_id)) == 0
    es_principal = data.es_principal or es_primera  # RN-DI01

    if es_principal:
        uow.direcciones.unset_principal(usuario_id)

    direccion = DireccionEntrega(
        usuario_id=usuario_id,
        alias=data.alias,
        linea1=data.linea1,
        linea2=data.linea2,
        es_principal=es_principal,
    )
    return uow.direcciones.create(direccion)


def update_direccion(
    uow: UnitOfWork, usuario_id: int, direccion_id: int, data: DireccionUpdate
) -> DireccionEntrega:
    direccion = _get_propia(uow, usuario_id, direccion_id)
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(direccion, key, value)
    return uow.direcciones.update(direccion)


def set_principal(uow: UnitOfWork, usuario_id: int, direccion_id: int) -> DireccionEntrega:
    direccion = _get_propia(uow, usuario_id, direccion_id)
    uow.direcciones.unset_principal(usuario_id)
    direccion.es_principal = True
    return uow.direcciones.update(direccion)


def delete_direccion(uow: UnitOfWork, usuario_id: int, direccion_id: int) -> None:
    direccion = _get_propia(uow, usuario_id, direccion_id)
    uow.direcciones.soft_delete(direccion)


def _get_propia(uow: UnitOfWork, usuario_id: int, direccion_id: int) -> DireccionEntrega:
    direccion = uow.direcciones.get_by_id(direccion_id)
    if not direccion or direccion.usuario_id != usuario_id:
        raise AppError(404, "Dirección no encontrada", "NOT_FOUND")
    return direccion
