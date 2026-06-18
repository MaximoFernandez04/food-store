"""
env.py de Alembic. A diferencia de un setup default, lee la URL desde
app.core.config.settings (que a su vez lee .env), no la pisa con un valor
hardcodeado, y registra los metadata de todos los modelos SQLModel para
que `alembic revision --autogenerate` los detecte.
"""
from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from app.core.config import settings

# Importar TODOS los módulos con modelos para que SQLModel.metadata los
# conozca antes del autogenerate. Sumar acá cada módulo nuevo.
from app.modules.usuarios import model as _usuarios_model  # noqa: F401
from app.modules.refreshtokens import model as _refreshtokens_model  # noqa: F401
from app.modules.categorias import model as _categorias_model  # noqa: F401
from app.modules.productos import model as _productos_model  # noqa: F401
from app.modules.direcciones import model as _direcciones_model  # noqa: F401
from app.modules.pedidos import model as _pedidos_model  # noqa: F401
from app.modules.pagos import model as _pagos_model  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def get_url() -> str:
    return settings.database_url


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    url = get_url()
    connect_args = {"client_encoding": "utf8"} if url.startswith("postgresql") else {}
    connectable = create_engine(url, connect_args=connect_args)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
