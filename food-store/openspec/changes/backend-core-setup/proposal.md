## Why

El código existente en `backend/` no puede ejecutarse: no hay `app/main.py`,
no hay `requirements.txt`, no hay configuración de Alembic ni `seed.py`. La
sesión de base de datos se creaba una sola vez a nivel de módulo (no es
thread-safe), `DATABASE_URL` apuntaba a SQLite hardcodeado y `SECRET_KEY`
estaba hardcodeada en el código fuente. Además existían archivos duplicados
y contradictorios (`models.py` vs `models/`, `routers/producto.py` vs
`routers/productos.py` con imports rotos a un módulo `backend.database`
inexistente).

Este change reconstruye la infraestructura base (`app/core/`) siguiendo
Feature-First, para que cada módulo de negocio (auth, productos, pedidos,
etc.) se pueda construir encima sin volver a tocar esta capa.

## What Changes

- Crea `app/main.py`, `requirements.txt`, `alembic.ini` + `alembic/env.py`
- `app/core/config.py`: Settings vía pydantic-settings, lee `.env`
- `app/core/database.py`: engine de Postgres + sesión por-request
  (`Depends(get_session)`), reemplaza al `SessionManager` global anterior
- `app/core/base_repository.py`: `BaseRepository[T]` genérico (sección 7.2)
- `app/core/uow.py`: Unit of Work con commit/rollback automático
- `app/core/security.py`: hashing bcrypt + JWT access/refresh
- `app/core/deps.py`: `get_current_user` / `require_role`
- `app/core/exceptions.py`: errores RFC 7807
- `app/core/rate_limit.py`: instancia compartida de slowapi
- Elimina (marcar para borrar manualmente en el repo real, ver tasks.md)
  los archivos duplicados/rotos de la implementación anterior

## Capabilities

### New Capabilities
- `backend-infrastructure`: engine, sesión por-request, UoW, BaseRepository,
  seguridad JWT/bcrypt, manejo de errores RFC 7807, rate limiting

## Impact

- Reemplaza por completo `backend/core/`, `backend/auth/jwt_handler.py` y
  `backend/auth/security.py` de la implementación anterior
- Bloqueante: ningún otro módulo (auth, productos, pedidos...) puede
  construirse sin esto
- Sin impacto en frontend todavía
