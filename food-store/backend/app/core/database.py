"""
Engine de SQLModel/PostgreSQL y dependencia de sesión.

IMPORTANTE — por qué esto reemplaza al `SessionManager` anterior:
El código viejo (`backend/core/database.py`) creaba UNA sola instancia de
`Session` a nivel de módulo, en el momento del import. Eso significa que
TODOS los requests concurrentes terminaban compartiendo la misma sesión de
SQLAlchemy, lo cual no es thread-safe y rompe bajo cualquier carga real.

Acá la sesión se crea (y cierra) por request, vía `Depends(get_session)`,
que es el patrón estándar de FastAPI + SQLModel.
"""
from typing import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine, expire_on_commit=False) as session:
        yield session
