## 1. Modelos

- [x] 1.1 `app/modules/usuarios/model.py`: Rol, Usuario, UsuarioRol
- [x] 1.2 `app/modules/refreshtokens/model.py`: RefreshToken (token_hash,
      expires_at, revoked_at)

## 2. Repositorios

- [x] 2.1 `UsuarioRepository`: get_by_email, get_roles, assign_role
- [x] 2.2 `RefreshTokenRepository`: get_by_hash, revoke

## 3. Service (stateless, recibe `uow` por parámetro)

- [x] 3.1 `register()`: valida email único, hashea password, asigna rol
      CLIENT automáticamente (NO acepta rol del input)
- [x] 3.2 `login()`: valida credenciales, emite access + refresh token
- [x] 3.3 `refresh()`: valida refresh token activo, lo revoca, emite par
      nuevo (rotación)
- [x] 3.4 `logout()`: revoca el refresh token recibido

## 4. Router

- [x] 4.1 `POST /api/v1/auth/register` → 201
- [x] 4.2 `POST /api/v1/auth/login` → 200, rate limited 5/15min (slowapi)
- [x] 4.3 `POST /api/v1/auth/refresh` → 200
- [x] 4.4 `POST /api/v1/auth/logout` → 204
- [x] 4.5 `GET /api/v1/auth/me` → 200, requiere Bearer

## 5. Seed

- [x] 5.1 `app/db/seed.py`: siembra los 4 roles + usuario admin
      (admin@foodstore.com / Admin1234!)

## 6. Validación manual (ver design.md — sin Postgres disponible se usó SQLite)

- [x] 6.1 register → 201, usuario creado con rol CLIENT
- [x] 6.2 login → 200, devuelve access_token + refresh_token
- [x] 6.3 me con Bearer válido → 200
- [x] 6.4 refresh → 200, emite par nuevo
- [x] 6.5 refresh con el token YA usado → 401 (rotación funciona)
- [x] 6.6 logout → 204
- [x] 6.7 6 logins fallidos seguidos → el 6to devuelve 429 (rate limit ok)
- [ ] 6.8 Repetir 6.1-6.7 contra PostgreSQL real antes de archivar el change
- [ ] 6.9 Agregar tests automatizados (pytest) — Epic 11
