"""
Lógica de negocio de Pagos. `mp_client` se importa como módulo (no se
importan sus funciones sueltas) para que los tests puedan mockear
`mp_client.crear_pago_mp` / `mp_client.consultar_pago_mp` sin pegarle a
la red real de MercadoPago.
"""
from uuid import uuid4

from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.pagos import mp_client
from app.modules.pagos.model import Pago
from app.modules.pagos.schema import CrearPagoRequest
from app.modules.pedidos.service import confirmar_por_pago

ESTADOS_PAGO_NO_FINALES = {"pending", "in_process"}


def crear_pago(uow: UnitOfWork, usuario_id: int, data: CrearPagoRequest) -> Pago:
    pedido = uow.pedidos.get_by_id(data.pedido_id)
    if not pedido or pedido.usuario_id != usuario_id:
        raise AppError(404, "Pedido no encontrado", "NOT_FOUND")
    if pedido.estado_codigo != "PENDIENTE":
        raise AppError(
            400,
            f"El pedido está en estado {pedido.estado_codigo}, no se puede pagar",
            "PEDIDO_NOT_PAYABLE",
        )

    idempotency_key = str(uuid4())  # RN-PA02: única por intento de pago

    mp_response = mp_client.crear_pago_mp(
        token=data.token,
        transaction_amount=float(pedido.total),
        description=f"Pedido #{pedido.id} - Food Store",
        external_reference=str(pedido.external_ref),  # RN-PA09
        idempotency_key=idempotency_key,
        payer_email=data.payer_email,
        installments=data.installments,
    )

    pago = Pago(
        pedido_id=pedido.id,
        mp_payment_id=mp_response.get("id"),
        mp_status=mp_response.get("status", "pending"),
        mp_status_detail=mp_response.get("status_detail"),
        external_reference=str(pedido.external_ref),
        idempotency_key=idempotency_key,
    )
    uow.pagos.create(pago)

    if pago.mp_status == "approved":  # RN-PA05
        confirmar_por_pago(uow, pedido.id)

    return pago


def procesar_webhook(uow: UnitOfWork, topic: str, mp_payment_id: int) -> None:
    """Llamada por el router del webhook IPN. RN-PA03: el router responde
    200 sin importar lo que pase acá adentro (ver router.py) — esta
    función puede lanzar AppError y el router lo absorbe sin romper la
    respuesta hacia MercadoPago.
    """
    if topic != "payment":
        return  # ignoramos otros topics (merchant_order, etc.)

    # RN-PA04: nunca confiar en el payload del webhook, siempre re-consultar.
    mp_data = mp_client.consultar_pago_mp(mp_payment_id)
    nuevo_status = mp_data.get("status", "pending")
    external_reference = mp_data.get("external_reference")

    pago = uow.pagos.get_by_mp_payment_id(mp_payment_id)

    if pago is None:
        # El webhook llegó antes de que tuviéramos registrado este pago
        # (caso borde). Lo asociamos por external_reference si existe el
        # pedido; si no podemos asociarlo, no hay nada seguro que hacer.
        if not external_reference:
            return
        pedido = uow.pedidos.get_by_external_ref(external_reference)
        if not pedido:
            return
        pago = Pago(
            pedido_id=pedido.id,
            mp_payment_id=mp_payment_id,
            mp_status=nuevo_status,
            mp_status_detail=mp_data.get("status_detail"),
            external_reference=external_reference,
            idempotency_key=str(uuid4()),
        )
        uow.pagos.create(pago)
    else:
        if pago.mp_status == nuevo_status:
            return  # RN-PA02: notificación duplicada, no hacer nada más
        pago.mp_status = nuevo_status
        pago.mp_status_detail = mp_data.get("status_detail")
        uow.pagos.update(pago)

    if nuevo_status == "approved":
        confirmar_por_pago(uow, pago.pedido_id)  # RN-PA05
    # rejected (RN-PA06), pending/in_process (RN-PA07): el pedido sigue
    # PENDIENTE, no hay transición de estado que disparar.
