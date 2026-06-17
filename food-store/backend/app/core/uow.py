"""
Unit of Work — sección 7 de la especificación.

Reemplaza al UnitOfWork viejo, que abría la sesión en el __init__ a nivel
de import y no garantizaba rollback consistente. Este UoW:
  - abre la sesión recién al entrar al `with`
  - expone los repositorios de cada módulo como atributos
  - hace commit() automático si no hubo excepción, rollback() si la hubo
  - el Service NUNCA llama session.commit() directamente (regla de la spec)

A medida que se agreguen módulos (productos, pedidos, pagos, etc.) se
suman acá sus repositorios siguiendo el mismo patrón.
"""
from types import TracebackType
from typing import Optional, Type

from sqlmodel import Session

from app.core.database import engine
from app.modules.categorias.repository import CategoriaRepository
from app.modules.direcciones.repository import DireccionRepository
from app.modules.pedidos.repository import (
    DetallePedidoRepository,
    EstadoPedidoRepository,
    FormaPagoRepository,
    HistorialRepository,
    PedidoRepository,
)
from app.modules.productos.repository import IngredienteRepository, ProductoRepository
from app.modules.refreshtokens.repository import RefreshTokenRepository
from app.modules.usuarios.repository import UsuarioRepository


class UnitOfWork:
    def __init__(self):
        self.session: Session = Session(engine, expire_on_commit=False)
        self.usuarios = UsuarioRepository(self.session)
        self.refresh_tokens = RefreshTokenRepository(self.session)
        self.categorias = CategoriaRepository(self.session)
        self.productos = ProductoRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        self.direcciones = DireccionRepository(self.session)
        self.pedidos = PedidoRepository(self.session)
        self.detalles = DetallePedidoRepository(self.session)
        self.historial = HistorialRepository(self.session)
        self.estados_pedido = EstadoPedidoRepository(self.session)
        self.formas_pago = FormaPagoRepository(self.session)

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def flush(self) -> None:
        self.session.flush()
