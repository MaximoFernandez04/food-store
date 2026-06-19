from decimal import Decimal

from pydantic import BaseModel


class ProductoMasVendido(BaseModel):
    producto_id: int
    nombre: str
    cantidad_vendida: int


class DashboardStats(BaseModel):
    total_ventas: Decimal
    pedidos_por_estado: dict[str, int]
    productos_mas_vendidos: list[ProductoMasVendido]
    total_usuarios: int
    total_productos: int
