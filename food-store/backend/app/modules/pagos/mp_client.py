"""
Wrapper delgado sobre el SDK oficial de MercadoPago. Se aísla en su propio
módulo a propósito: permite mockear estas dos funciones en tests sin
necesidad de pegarle a la red real, y si el día de mañana cambia el SDK
o la versión de la API, el cambio queda contenido acá.
"""
import mercadopago

from app.core.config import settings


def _get_sdk() -> mercadopago.SDK:
    return mercadopago.SDK(settings.mp_access_token)


def crear_pago_mp(
    token: str,
    transaction_amount: float,
    description: str,
    external_reference: str,
    idempotency_key: str,
    payer_email: str,
    installments: int = 1,
) -> dict:
    """Crea el pago en MercadoPago. `token` es el card_token generado por
    el SDK MercadoPago.js en el navegador (RN-AU09/RN-PA01): los datos de
    tarjeta NUNCA llegan a este backend.
    """
    sdk = _get_sdk()
    payment_data = {
        "transaction_amount": transaction_amount,
        "token": token,
        "description": description,
        "installments": installments,
        "payer": {"email": payer_email},
        "external_reference": external_reference,
    }
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {"x-idempotency-key": idempotency_key}
    response = sdk.payment().create(payment_data, request_options)
    return response["response"]


def consultar_pago_mp(mp_payment_id: int) -> dict:
    """RN-PA04: el webhook nunca confía ciegamente en el payload de la
    notificación IPN — siempre re-consulta el estado real contra la API
    de MercadoPago antes de actuar."""
    sdk = _get_sdk()
    response = sdk.payment().get(mp_payment_id)
    return response["response"]
