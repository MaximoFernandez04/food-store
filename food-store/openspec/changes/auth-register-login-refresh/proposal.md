## Why

La implementación anterior de auth (`backend/auth/`, `backend/routers/auth.py`)
tenía varios problemas bloqueantes respecto a la spec v5.0:

- `SECRET_KEY` hardcodeada en el código fuente en vez de leerse de `.env`.
- No existía `/auth/refresh` ni `/auth/logout` reales: no había tabla
  `RefreshToken`, por lo que era imposible invalidar una sesión.
- No había rate limiting en `/auth/login` (la spec exige 5 intentos
  fallidos por IP en 15 minutos vía slowapi).
- El registro pedía `role` como input del cliente (`RegisterRequest.role`),
  lo cual permite que cualquiera se autoregistre como ADMIN. La spec
  exige que todo usuario nuevo se asigne el rol CLIENT por defecto.
- Los roles no usaban la tabla pivot `usuario_rol` (RBAC real, M:N);
  estaban como un campo `role: str` suelto en `Usuario`.

## What Changes

- Nuevo módulo `app/modules/usuarios/`: modelos `Rol`, `Usuario`,
  `UsuarioRol` (M:N real) + repositorio
- Nuevo módulo `app/modules/refreshtokens/`: modelo `RefreshToken`
  (token_hash SHA-256, nunca el token plano) + repositorio
- Nuevo módulo `app/modules/auth/`: schemas, service (stateless, recibe
  `uow` por parámetro) y router con:
  - `POST /api/v1/auth/register` → asigna rol `CLIENT` automáticamente
  - `POST /api/v1/auth/login` → rate limited 5/15min, devuelve access +
    refresh token
  - `POST /api/v1/auth/refresh` → rota el refresh token (el usado queda
    revocado, se emite uno nuevo)
  - `POST /api/v1/auth/logout` → revoca el refresh token (`revoked_at`)
  - `GET /api/v1/auth/me` → requiere Bearer token

## Capabilities

### New Capabilities
- `auth`: registro, login, refresh con rotación, logout, RBAC base (rol
  CLIENT asignado automáticamente; asignación de otros roles queda para
  `rbac-role-management`, el siguiente change del roadmap)

## Impact

- Reemplaza `backend/auth/`, `backend/routers/auth.py`,
  `backend/schemas/auth_schema.py` de la implementación anterior
- Depende de `backend-core-setup` (ya aplicado)
- Desbloquea `auth-logout` (ya incluido acá, ver nota en tasks.md) y
  `rbac-role-management`
