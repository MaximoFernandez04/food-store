from fastapi import APIRouter, Depends, Query, status

from app.core.deps import CurrentUser, get_current_user
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.pedidos import service
from app.modules.pedidos.schema import (
    AvanzarEstadoRequest,
    CrearPedidoRequest,
    HistorialRead,
    PaginatedPedidos,
    PedidoDetail,
    PedidoRead,
)

router = APIRouter(prefix="/api/v1/pedidos", tags=["pedidos"])

ROLES_STAFF = {"ADMIN", "PEDIDOS"}


@router.get("", response_model=PaginatedPedidos)
def list_pedidos(
    estado: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    current: CurrentUser = Depends(get_current_user),
):
    # CLIENT ve solo los propios; ADMIN/PEDIDOS ven todos.
    es_staff = current.has_role(*ROLES_STAFF)
    usuario_filtro = None if es_staff else current.usuario.id
    with UnitOfWork() as uow:
        items, total = uow.pedidos.search(usuario_filtro, estado, page, size)
        return PaginatedPedidos(items=items, total=total, page=page, size=size)


@router.get("/{pedido_id}", response_model=PedidoDetail)
def get_pedido(pedido_id: int, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if not pedido:
            raise AppError(404, "Pedido no encontrado", "NOT_FOUND")
        if not current.has_role(*ROLES_STAFF) and pedido.usuario_id != current.usuario.id:
            raise AppError(403, "No podés ver pedidos de otro usuario", "FORBIDDEN")

        items = uow.detalles.list_by_pedido(pedido_id)
        historial = uow.historial.list_by_pedido(pedido_id)
        return PedidoDetail(**pedido.model_dump(), items=items, historial=historial)


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_pedido(data: CrearPedidoRequest, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        return service.crear_pedido(uow, current.usuario.id, data)


@router.patch("/{pedido_id}/estado", response_model=PedidoRead)
def avanzar_estado(
    pedido_id: int, data: AvanzarEstadoRequest, current: CurrentUser = Depends(get_current_user)
):
    with UnitOfWork() as uow:
        return service.avanzar_estado(uow, pedido_id, current, data)


@router.get("/{pedido_id}/historial", response_model=list[HistorialRead])
def get_historial(pedido_id: int, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if not pedido:
            raise AppError(404, "Pedido no encontrado", "NOT_FOUND")
        if not current.has_role(*ROLES_STAFF) and pedido.usuario_id != current.usuario.id:
            raise AppError(403, "No podés ver el historial de pedidos de otro usuario", "FORBIDDEN")
        return uow.historial.list_by_pedido(pedido_id)
