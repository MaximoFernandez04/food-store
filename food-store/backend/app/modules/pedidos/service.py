"""
Lógica de negocio de Pedidos. Implementa:
- RN-01/02/03/05 (PDF) y RN-FS01 a RN-FS09 + RN-PE01 a RN-PE08 (Historias)
- Snapshot de precio/nombre/dirección al crear (inmutable)
- Stock: se VALIDA al crear (con lock de fila), se DESCUENTA al confirmar
  (no al crear) — RN-FS03. Si se cancela un pedido ya CONFIRMADO, el stock
  se restaura (RN-FS05).
- HistorialEstadoPedido append-only: cada transición es un INSERT nuevo,
  nunca se actualiza un registro existente.
"""
from decimal import Decimal

from app.core.deps import CurrentUser
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.pedidos.model import DetallePedido, HistorialEstadoPedido, Pedido
from app.modules.pedidos.schema import AvanzarEstadoRequest, CrearPedidoRequest

COSTO_ENVIO_FIJO = Decimal("50.00")

# RN-FS01/RN-FS06: mapa de transiciones válidas. ENTREGADO y CANCELADO son
# terminales (no aparecen como clave = sin transiciones salientes).
TRANSICIONES_VALIDAS: dict[str, set[str]] = {
    "PENDIENTE": {"CONFIRMADO", "CANCELADO"},
    "CONFIRMADO": {"EN_PREPARACION", "CANCELADO"},
    "EN_PREPARACION": {"EN_CAMINO", "CANCELADO"},
    "EN_CAMINO": {"ENTREGADO"},
}

ROLES_GESTION_PEDIDOS = {"ADMIN", "PEDIDOS"}


def crear_pedido(uow: UnitOfWork, usuario_id: int, data: CrearPedidoRequest) -> Pedido:
    direccion_texto = None
    if data.direccion_id is not None:
        direccion = uow.direcciones.get_by_id(data.direccion_id)
        if not direccion or direccion.usuario_id != usuario_id:
            raise AppError(404, "Dirección no encontrada", "DIRECCION_NOT_FOUND")
        direccion_texto = direccion.linea1 + (f", {direccion.linea2}" if direccion.linea2 else "")

    forma_pago = uow.formas_pago.get_by_id(data.forma_pago_codigo)
    if not forma_pago or not forma_pago.habilitado:
        raise AppError(400, "Forma de pago inválida o deshabilitada", "INVALID_FORMA_PAGO", "forma_pago_codigo")

    subtotal = Decimal("0.00")
    items_a_crear: list[tuple] = []  # (producto, item_request, item_subtotal)

    for item in data.items:
        # RN-PE04: lock de fila (SELECT FOR UPDATE) para evitar que dos
        # pedidos concurrentes vendan el mismo stock dos veces.
        producto = uow.productos.get_by_id_for_update(item.producto_id)
        if not producto or not producto.disponible:
            # RN-PE05: todo o nada. Levantar la excepción acá aborta TODA
            # la transacción (el UoW hace rollback) — no se crea ningún
            # ítem aunque los anteriores hayan pasado la validación.
            raise AppError(404, f"Producto {item.producto_id} no disponible", "PRODUCT_NOT_AVAILABLE")
        if producto.stock_cantidad < item.cantidad:
            raise AppError(
                400, f"Stock insuficiente para '{producto.nombre}'", "INSUFFICIENT_STOCK"
            )

        if item.personalizacion:
            ingredientes_validos = {i.id for i in uow.productos.ingredientes_de(producto.id)}
            if not set(item.personalizacion).issubset(ingredientes_validos):
                raise AppError(
                    400,
                    "La personalización incluye ingredientes que el producto no tiene",
                    "INVALID_CUSTOMIZATION",
                )

        item_subtotal = producto.precio_base * item.cantidad
        subtotal += item_subtotal
        items_a_crear.append((producto, item, item_subtotal))

    total = subtotal + COSTO_ENVIO_FIJO

    pedido = Pedido(
        usuario_id=usuario_id,
        estado_codigo="PENDIENTE",
        forma_pago_codigo=data.forma_pago_codigo,
        direccion_id=data.direccion_id,
        direccion_texto_snapshot=direccion_texto,
        subtotal=subtotal,
        costo_envio=COSTO_ENVIO_FIJO,
        total=total,
        notas=data.notas,
    )
    uow.pedidos.create(pedido)  # flush() interno -> pedido.id disponible

    for producto, item, item_subtotal in items_a_crear:
        # RN-PE02: snapshot de nombre y precio, inmutable a futuro.
        uow.detalles.create(
            DetallePedido(
                pedido_id=pedido.id,
                producto_id=producto.id,
                nombre_snapshot=producto.nombre,
                precio_snapshot=producto.precio_base,
                cantidad=item.cantidad,
                subtotal=item_subtotal,
                personalizacion=item.personalizacion,
            )
        )

    # RN-02/RN-PE06: primer registro de historial con estado_desde=None.
    uow.historial.create(
        HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_desde=None,
            estado_hasta="PENDIENTE",
            usuario_id=usuario_id,
        )
    )
    return pedido


def _descontar_stock(uow: UnitOfWork, pedido: Pedido) -> None:
    detalles = uow.detalles.list_by_pedido(pedido.id)
    for detalle in detalles:
        # RN-FS03/04: descuento atómico; si CUALQUIER producto no tiene
        # stock suficiente a esta altura, se aborta todo (rollback del UoW).
        producto = uow.productos.get_by_id_for_update(detalle.producto_id)
        if not producto or producto.stock_cantidad < detalle.cantidad:
            raise AppError(
                409,
                f"Stock insuficiente para confirmar (producto {detalle.producto_id})",
                "INSUFFICIENT_STOCK_ON_CONFIRM",
            )
        producto.stock_cantidad -= detalle.cantidad
        uow.productos.update(producto)


def confirmar_por_pago(uow: UnitOfWork, pedido_id: int) -> Pedido:
    """Única vía para PENDIENTE -> CONFIRMADO cuando la forma de pago es
    MERCADOPAGO (RN-FS02). La llama el módulo de pagos cuando MercadoPago
    confirma un pago aprobado — nunca un router de pedidos. usuario_id=None
    en el historial = transición del Sistema."""
    pedido = uow.pedidos.get_by_id_for_update(pedido_id)
    if not pedido:
        raise AppError(404, "Pedido no encontrado", "NOT_FOUND")

    if pedido.estado_codigo != "PENDIENTE":
        return pedido  # idempotencia: webhook duplicado, no hacer nada raro

    _descontar_stock(uow, pedido)
    _aplicar_transicion(uow, pedido, "CONFIRMADO", usuario_id=None, motivo="Pago aprobado")
    return pedido


def avanzar_estado(
    uow: UnitOfWork, pedido_id: int, current: CurrentUser, data: AvanzarEstadoRequest
) -> Pedido:
    pedido = uow.pedidos.get_by_id_for_update(pedido_id)
    if not pedido:
        raise AppError(404, "Pedido no encontrado", "NOT_FOUND")

    estado_actual = pedido.estado_codigo
    nuevo_estado = data.nuevo_estado

    if nuevo_estado == "CONFIRMADO":
        if pedido.forma_pago_codigo == "MERCADOPAGO":
            # RN-FS02: para MercadoPago esta transición es EXCLUSIVAMENTE
            # automática (la dispara el webhook de pago aprobado).
            raise AppError(
                403,
                "Este pedido se paga con MercadoPago: la confirmación es automática al aprobarse el pago",
                "MANUAL_CONFIRM_FORBIDDEN",
            )
        # EFECTIVO/TRANSFERENCIA no tienen gateway que dispare un webhook,
        # así que el staff confirma a mano que cobró/recibió la transferencia.
        if estado_actual != "PENDIENTE":
            raise AppError(400, f"Transición inválida: {estado_actual} → CONFIRMADO", "INVALID_TRANSITION")
        if not current.has_role(*ROLES_GESTION_PEDIDOS):
            raise AppError(403, "Requiere rol ADMIN o PEDIDOS", "FORBIDDEN")
        _descontar_stock(uow, pedido)
        _aplicar_transicion(uow, pedido, "CONFIRMADO", current.usuario.id, motivo="Pago confirmado manualmente")
        return pedido

    if nuevo_estado not in TRANSICIONES_VALIDAS.get(estado_actual, set()):
        raise AppError(
            400,
            f"Transición inválida: {estado_actual} → {nuevo_estado}",
            "INVALID_TRANSITION",
        )

    if nuevo_estado == "CANCELADO":
        if not data.motivo:
            raise AppError(400, "El motivo es obligatorio al cancelar", "MOTIVO_REQUERIDO", "motivo")
        _validar_permiso_cancelacion(pedido, estado_actual, current)
        # RN-FS05: el stock se descuenta al llegar a CONFIRMADO (RN-FS03) y
        # permanece descontado en los estados posteriores. Si se cancela
        # desde CONFIRMADO o desde EN_PREPARACION, en ambos casos el stock
        # ya estaba descontado y hay que restaurarlo. Solo si se cancela
        # desde PENDIENTE no hay nada que restaurar (nunca se descontó).
        if estado_actual in {"CONFIRMADO", "EN_PREPARACION"}:
            _restaurar_stock(uow, pedido.id)
    else:
        # Transiciones de avance normal (CONFIRMADO→EN_PREPARACION, etc.):
        # solo ADMIN o PEDIDOS (RN-RB07/RN-RB09).
        if not current.has_role(*ROLES_GESTION_PEDIDOS):
            raise AppError(403, "Requiere rol ADMIN o PEDIDOS", "FORBIDDEN")

    _aplicar_transicion(uow, pedido, nuevo_estado, current.usuario.id, data.motivo)
    return pedido


def _validar_permiso_cancelacion(pedido: Pedido, estado_actual: str, current: CurrentUser) -> None:
    es_propietario = pedido.usuario_id == current.usuario.id

    if estado_actual == "PENDIENTE":
        # Cliente propietario, o Gestor de Pedidos, o Admin (RN-FS08).
        if current.has_role("ADMIN", "PEDIDOS"):
            return
        if current.has_role("CLIENT") and es_propietario:
            return
        raise AppError(403, "No podés cancelar este pedido", "FORBIDDEN")

    if estado_actual == "CONFIRMADO":
        # Solo Gestor de Pedidos o Admin, NO el cliente (RN-FS08).
        if current.has_role("ADMIN", "PEDIDOS"):
            return
        raise AppError(403, "Solo ADMIN o PEDIDOS pueden cancelar un pedido CONFIRMADO", "FORBIDDEN")

    if estado_actual == "EN_PREPARACION":
        # RN-RB08: solo ADMIN, ni siquiera el Gestor de Pedidos.
        if current.has_role("ADMIN"):
            return
        raise AppError(403, "Solo ADMIN puede cancelar un pedido EN_PREPARACION", "FORBIDDEN")

    raise AppError(400, f"No se puede cancelar un pedido en estado {estado_actual}", "INVALID_TRANSITION")


def _restaurar_stock(uow: UnitOfWork, pedido_id: int) -> None:
    for detalle in uow.detalles.list_by_pedido(pedido_id):
        producto = uow.productos.get_by_id_for_update(detalle.producto_id)
        if producto:
            producto.stock_cantidad += detalle.cantidad
            uow.productos.update(producto)


def _aplicar_transicion(
    uow: UnitOfWork, pedido: Pedido, nuevo_estado: str, usuario_id: int | None, motivo: str | None
) -> None:
    estado_anterior = pedido.estado_codigo
    pedido.estado_codigo = nuevo_estado
    uow.pedidos.update(pedido)
    # RN-03/RN-FS07: append-only. Esto es siempre un INSERT nuevo, nunca un
    # UPDATE sobre un registro de historial existente.
    uow.historial.create(
        HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_desde=estado_anterior,
            estado_hasta=nuevo_estado,
            usuario_id=usuario_id,
            motivo=motivo,
        )
    )
