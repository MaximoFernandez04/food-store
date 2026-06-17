## Decisiones de diseño

### Rotación de refresh token
Cada `/auth/refresh` exitoso revoca el token usado y emite uno nuevo. Es
más seguro que reusar el mismo refresh token durante los 7 días: si un
token robado se usa una vez, el legítimo deja de funcionar en el próximo
intento del usuario real, lo cual es una señal detectable (no implementada
en este change: alertar al usuario o forzar logout global queda fuera de
alcance, podría ser un change futuro de seguridad).

### Rol por defecto en registro
`RegisterRequest` ya NO acepta `role` como input (en el código anterior sí,
lo cual era una vulnerabilidad de escalación de privilegios). Todo registro
público crea un usuario con rol `CLIENT` únicamente. La asignación de
roles ADMIN/STOCK/PEDIDOS queda para el módulo `admin-gestionar-usuarios`
(Epic 10 de `docs/CHANGES.md`), protegido por `require_role(["ADMIN"])`.

### `auth-logout` fusionado en este change
`docs/CHANGES.md` lista `auth-logout` como change separado dependiente de
este. Se decidió implementarlo en el mismo change porque el modelo
`RefreshToken` (con su campo `revoked_at`) ya se estaba creando acá y
separarlo hubiera significado tocar el mismo archivo dos veces sin
beneficio real. Se documenta la fusión acá para que quede trazado.

### Roles en el JWT vs. consulta a BD en cada request
Los roles se embeben en el payload del access token (`roles: list[str]`)
para no pegarle a la base en cada request protegido. Esto significa que si
un ADMIN le revoca el rol a un usuario, el cambio no tiene efecto hasta que
el access token actual expire (máx. 30 min). Se considera un trade-off
aceptable para v5.0; si se necesitara revocación inmediata, habría que
consultar roles en cada request o mantener una lista de invalidación.

## Riesgos / Trade-offs

- No hay tests automatizados todavía (se validó manualmente con
  `TestClient` de FastAPI contra SQLite in-memory). `tests-pytest-coverage`
  sigue pendiente como change de Epic 11.
- Falta el flujo de "olvidé mi contraseña" — no está en la spec v5.0 ni en
  `docs/CHANGES.md`, así que no se implementa.
