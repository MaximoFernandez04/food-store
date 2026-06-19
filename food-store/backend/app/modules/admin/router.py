from fastapi import APIRouter, Depends

from app.core.deps import CurrentUser, get_current_user
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.admin import service
from app.modules.admin.schema import DashboardStats

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(current: CurrentUser = Depends(get_current_user)):
    # Ventas y métricas financieras: solo ADMIN (RBAC — ni STOCK ni PEDIDOS
    # tienen acceso a datos financieros según la tabla de roles).
    if not current.has_role("ADMIN"):
        raise AppError(403, "Requiere rol ADMIN", "FORBIDDEN")
    with UnitOfWork() as uow:
        return service.get_dashboard_stats(uow)
