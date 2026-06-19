"""
Dashboard de métricas para el panel de Admin. Son agregaciones de solo
lectura sobre tablas que ya existen (Pedido, DetallePedido, Usuario,
Producto) — no hay un modelo propio ni tabla nueva, así que se consulta
directo vía uow.session en vez de sumar una capa de repository para un
único endpoint de lectura.
"""
from sqlmodel import func, select

from app.core.uow import UnitOfWork
from app.modules.admin.schema import DashboardStats, ProductoMasVendido
from app.modules.pedidos.model import DetallePedido, Pedido
from app.modules.productos.model import Producto
from app.modules.usuarios.model import Usuario

ESTADOS_PEDIDO_ORDENADOS = [
    "PENDIENTE",
    "CONFIRMADO",
    "EN_PREPARACION",
    "EN_CAMINO",
    "ENTREGADO",
    "CANCELADO",
]


def get_dashboard_stats(uow: UnitOfWork) -> DashboardStats:
    session = uow.session

    total_ventas = session.exec(
        select(func.coalesce(func.sum(Pedido.total), 0)).where(Pedido.estado_codigo != "CANCELADO")
    ).one()

    conteo_por_estado = dict(
        session.exec(select(Pedido.estado_codigo, func.count(Pedido.id)).group_by(Pedido.estado_codigo)).all()
    )
    pedidos_por_estado = {estado: conteo_por_estado.get(estado, 0) for estado in ESTADOS_PEDIDO_ORDENADOS}

    top_productos = session.exec(
        select(
            DetallePedido.producto_id,
            DetallePedido.nombre_snapshot,
            func.sum(DetallePedido.cantidad).label("total_vendido"),
        )
        .group_by(DetallePedido.producto_id, DetallePedido.nombre_snapshot)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .limit(5)
    ).all()

    total_usuarios = session.exec(select(func.count(Usuario.id)).where(Usuario.deleted_at.is_(None))).one()
    total_productos = session.exec(select(func.count(Producto.id)).where(Producto.deleted_at.is_(None))).one()

    return DashboardStats(
        total_ventas=total_ventas,
        pedidos_por_estado=pedidos_por_estado,
        productos_mas_vendidos=[
            ProductoMasVendido(producto_id=p[0], nombre=p[1], cantidad_vendida=p[2]) for p in top_productos
        ],
        total_usuarios=total_usuarios,
        total_productos=total_productos,
    )
