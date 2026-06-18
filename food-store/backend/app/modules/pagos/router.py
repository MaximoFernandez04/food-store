import traceback

from fastapi import APIRouter, Depends, Request, status

from app.core.deps import CurrentUser, get_current_user
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.pagos import service
from app.modules.pagos.schema import CrearPagoRequest, PagoResponse

router = APIRouter(prefix="/api/v1/pagos", tags=["pagos"])


@router.post("/crear", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(data: CrearPagoRequest, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        return service.crear_pago(uow, current.usuario.id, data)


@router.post("/webhook")
async def webhook(request: Request):
    """Endpoint público (sin auth) — lo llama MercadoPago, no un humano.
    RN-PA03: SIEMPRE responde 200 de inmediato, incluso si el procesamiento
    interno falla, para que MercadoPago no reintente indefinidamente. Los
    errores se loguean (acá con print; en producción real iría a un logger
    o servicio de monitoreo) en vez de propagarse al cliente HTTP.

    NOTA DE SEGURIDAD: en producción habría que validar la firma del
    webhook (header `x-signature`) contra el secret de la app de MP antes
    de confiar en la notificación. No está implementado en esta versión
    por el tiempo acotado del TPI — queda documentado como deuda conocida.
    """
    params = request.query_params
    topic = params.get("topic") or params.get("type")
    mp_payment_id = params.get("id") or params.get("data.id")

    if topic and mp_payment_id:
        try:
            with UnitOfWork() as uow:
                service.procesar_webhook(uow, topic, int(mp_payment_id))
        except Exception:
            traceback.print_exc()

    return {"status": "ok"}


@router.get("/{pedido_id}", response_model=PagoResponse)
def get_pago(pedido_id: int, current: CurrentUser = Depends(get_current_user)):
    with UnitOfWork() as uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if not pedido:
            raise AppError(404, "Pedido no encontrado", "NOT_FOUND")
        if not current.has_role("ADMIN", "PEDIDOS") and pedido.usuario_id != current.usuario.id:
            raise AppError(403, "No podés ver el pago de otro usuario", "FORBIDDEN")

        pago = uow.pagos.get_ultimo_de_pedido(pedido_id)
        if not pago:
            raise AppError(404, "No hay pagos registrados para este pedido", "NOT_FOUND")
        return pago
