"""
Seed data obligatorio (sección 10.2). Ejecutar una vez después de
`alembic upgrade head`:

    python -m app.db.seed

Roles: completos. EstadoPedido y FormaPago se agregan cuando se sumen
los módulos productos/pedidos (quedan listados como TODO abajo para no
perder de vista que la spec los exige).
"""
from sqlmodel import Session, select

from app.core.database import engine
from app.core.security import hash_password
from app.modules.usuarios.model import Rol, Usuario, UsuarioRol

# Importa TODOS los módulos con modelos SQLModel antes de tocar la sesión.
# Necesario porque Usuario.refresh_tokens referencia "RefreshToken" como
# string (forward ref entre módulos distintos): si este módulo no se
# importa en algún punto antes de la primera query, SQLAlchemy no puede
# resolver el nombre al armar los mappers y tira InvalidRequestError.
# app/main.py y alembic/env.py ya hacen este mismo import por la misma razón.
from app.modules.refreshtokens import model as _refreshtokens_model  # noqa: F401
from app.modules.categorias import model as _categorias_model  # noqa: F401
from app.modules.productos import model as _productos_model  # noqa: F401
from app.modules.direcciones import model as _direcciones_model  # noqa: F401
from app.modules.pedidos.model import EstadoPedido, FormaPago

ROLES = [
    ("ADMIN", "Administrador"),
    ("STOCK", "Gestor de Stock"),
    ("PEDIDOS", "Gestor de Pedidos"),
    ("CLIENT", "Cliente"),
]

# (codigo, descripcion, orden, es_terminal) — orden estable, se referencia
# en la FSM de app/modules/pedidos/service.py.
ESTADOS_PEDIDO = [
    ("PENDIENTE", "Pedido creado, pago pendiente", 1, False),
    ("CONFIRMADO", "Pago procesado y confirmado", 2, False),
    ("EN_PREPARACION", "En preparación en cocina", 3, False),
    ("EN_CAMINO", "Despachado al cliente", 4, False),
    ("ENTREGADO", "Entrega confirmada", 5, True),
    ("CANCELADO", "Pedido cancelado", 6, True),
]

FORMAS_PAGO = [
    ("MERCADOPAGO", "MercadoPago (tarjeta, Rapipago, Pago Fácil)"),
    ("EFECTIVO", "Efectivo al recibir"),
    ("TRANSFERENCIA", "Transferencia bancaria"),
]

ADMIN_EMAIL = "admin@foodstore.com"
ADMIN_PASSWORD = "Admin1234!"  # cambiar en producción


def seed_roles(session: Session) -> None:
    for codigo, descripcion in ROLES:
        if not session.get(Rol, codigo):
            session.add(Rol(codigo=codigo, descripcion=descripcion))
    session.commit()


def seed_estados_pedido(session: Session) -> None:
    for codigo, descripcion, orden, es_terminal in ESTADOS_PEDIDO:
        if not session.get(EstadoPedido, codigo):
            session.add(
                EstadoPedido(
                    codigo=codigo, descripcion=descripcion, orden=orden, es_terminal=es_terminal
                )
            )
    session.commit()


def seed_formas_pago(session: Session) -> None:
    for codigo, descripcion in FORMAS_PAGO:
        if not session.get(FormaPago, codigo):
            session.add(FormaPago(codigo=codigo, descripcion=descripcion, habilitado=True))
    session.commit()


def seed_admin(session: Session) -> None:
    statement = select(Usuario).where(Usuario.email == ADMIN_EMAIL)
    existing = session.exec(statement).first()
    if existing:
        return

    admin = Usuario(
        nombre="Admin",
        apellido="FoodStore",
        email=ADMIN_EMAIL,
        password_hash=hash_password(ADMIN_PASSWORD),
    )
    session.add(admin)
    session.flush()
    session.add(UsuarioRol(usuario_id=admin.id, rol_codigo="ADMIN"))
    session.commit()


def run():
    with Session(engine) as session:
        seed_roles(session)
        seed_estados_pedido(session)
        seed_formas_pago(session)
        seed_admin(session)
    print("Seed completo: roles + estados de pedido + formas de pago + usuario admin.")


if __name__ == "__main__":
    run()
