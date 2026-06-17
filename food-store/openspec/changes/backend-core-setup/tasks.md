## 1. Infraestructura base

- [x] 1.1 `app/main.py` con CORS, exception handlers (RFC7807 + rate limit), health check
- [x] 1.2 `requirements.txt` con versiones acordes a la spec v5.0
- [x] 1.3 `app/core/config.py` (Settings desde `.env`)
- [x] 1.4 `app/core/database.py` (engine Postgres + sesión por-request)
- [x] 1.5 `app/core/base_repository.py` (genérico)
- [x] 1.6 `app/core/uow.py` (Unit of Work)
- [x] 1.7 `app/core/security.py` (bcrypt + JWT access/refresh)
- [x] 1.8 `app/core/deps.py` (get_current_user, require_role)
- [x] 1.9 `app/core/exceptions.py` (RFC 7807)
- [x] 1.10 `app/core/rate_limit.py` (slowapi)

## 2. Alembic

- [x] 2.1 `alembic.ini` + `alembic/env.py` apuntando a `settings.database_url`
- [ ] 2.2 Generar migración inicial contra Postgres real:
      `alembic revision --autogenerate -m "init"` (pendiente: requiere
      Postgres corriendo, no disponible en este entorno)
- [ ] 2.3 `alembic upgrade head` contra la base del equipo

## 3. Limpieza de la implementación anterior

- [ ] 3.1 Borrar `backend/models.py`, `backend/schemas.py` (raíz, duplicados)
- [ ] 3.2 Borrar `backend/routers/productos.py` (import roto a
      `backend.database`, reemplazado por el módulo `productos` nuevo)
- [ ] 3.3 Borrar `backend/routers/ordenes.py`, `backend/routers/order.py`
      (duplicados/contradictorios, reemplazados por módulo `pedidos`)
- [ ] 3.4 Borrar `backend/services/orden_service.py` (usa SQLAlchemy
      directo, no UoW)
- [ ] 3.5 Decidir si migrar o descartar `backend/models/`, `backend/auth/`,
      `backend/repositories/`, `backend/services/`, `backend/schemas/`
      viejos (reemplazados por `app/modules/...`)

## 4. Validación

- [x] 4.1 `pip install -r requirements.txt` sin errores
- [x] 4.2 La app importa y registra rutas sin excepciones
- [x] 4.3 `SQLModel.metadata.create_all()` crea las tablas sin error
- [ ] 4.4 Validar contra Postgres real (no SQLite) antes de archivar
