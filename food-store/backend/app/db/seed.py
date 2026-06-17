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

ROLES = [
    ("ADMIN", "Administrador"),
    ("STOCK", "Gestor de Stock"),
    ("PEDIDOS", "Gestor de Pedidos"),
    ("CLIENT", "Cliente"),
]

ADMIN_EMAIL = "admin@foodstore.com"
ADMIN_PASSWORD = "Admin1234!"  # cambiar en producción


def seed_roles(session: Session) -> None:
    for codigo, descripcion in ROLES:
        if not session.get(Rol, codigo):
            session.add(Rol(codigo=codigo, descripcion=descripcion))
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
        seed_admin(session)
    print("Seed completo: roles + usuario admin.")
    print("TODO (cuando existan los módulos correspondientes):")
    print("  - EstadoPedido: PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO")
    print("  - FormaPago: MERCADOPAGO, EFECTIVO, TRANSFERENCIA")


if __name__ == "__main__":
    run()
