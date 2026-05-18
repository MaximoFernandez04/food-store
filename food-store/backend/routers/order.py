from fastapi import APIRouter, Depends, HTTPException, status
from backend.repositories.orden_repository import OrdenRepository
from backend.services.order_fsm_service import OrderFsmService
from backend.models.orden import Orden
from backend.core.unit_of_work import UnitOfWork
from backend.auth.dependencies import get_current_user
from backend.auth.role_checker import verify_role
from backend.schemas.orden_schema import OrdenResponse

router = APIRouter()

@router.patch("/ordenes/{id}/estado", response_model=OrdenResponse)
def update_order_state(
    id: int,
    new_state: str,
    uow: UnitOfWork = Depends(),
    user = Depends(get_current_user),
):
    orden_repository = uow.orden_repository
    order_fsm_service = OrderFsmService(orden_repository)

    # Obtener orden
    order = orden_repository.get_by_id(id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Orden con ID {id} no encontrada"
        )

    # Validación por roles
    if user.role == "CLIENTE":
        if order.estado != "PENDIENTE" or new_state != "CANCELADO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clientes solo pueden cancelar órdenes pendientes",
            )

    elif user.role == "GESTOR_PEDIDOS":
        if new_state not in ["PAGADO", "PREPARANDO", "ENVIADO", "ENTREGADO"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gestores de pedidos solo pueden avanzar estados",
            )

    # Actualizar uso de FSM
    updated_order = order_fsm_service.update_state(order, new_state)

    uow.commit()
    return updated_order