## Context

La spec v5.0 exige PostgreSQL, variables de entorno, UoW con
BaseRepository genérico y errores RFC 7807. Nada de esto existía operativo.

## Decisiones de diseño

### 1. Sesión por-request, no global
El código anterior instanciaba `Session(engine)` una sola vez al importar
el módulo. Se reemplaza por `get_session()` (dependencia de FastAPI) y,
para el patrón UoW, por una sesión nueva en cada `with UnitOfWork():`.

### 2. `expire_on_commit=False`
Decisión tomada tras detectar `DetachedInstanceError` en testing: SQLAlchemy
expira los atributos de los objetos al hacer `commit()` por defecto, lo que
rompe cuando el Router accede al objeto retornado por el Service *después*
de que el UoW ya cerró la sesión. Se desactiva ese comportamiento en la
sesión del UoW y en `get_session()`.

### 3. `bcrypt==4.0.1` pineado
`passlib` (la librería que pide la spec) tiene un bug de compatibilidad
conocido con `bcrypt>=4.1` (falla al verificar el "wrap bug" interno).
Se pinea la versión hasta que el ecosistema lo resuelva.

### 4. Refresh token con rotación
Cada `POST /auth/refresh` revoca el refresh token usado y emite uno nuevo
(rotación). Esto no estaba en la implementación anterior (no existía
`/auth/refresh` funcional). Reduce la ventana de uso de un token robado.

### 5. BaseRepository[T] genérico vive en `core/`, no en cada módulo
Cada repositorio concreto (`UsuarioRepository`, etc.) hereda de
`BaseRepository[T]` y solo define sus queries específicas
(`get_by_email`, etc.), como pide la sección 7.2.

## Riesgos / Trade-offs

- No se generó la migración inicial de Alembic contra Postgres real (no
  hay servidor Postgres disponible en este entorno). `alembic/env.py` está
  listo; falta correr `alembic revision --autogenerate -m "init"` contra
  una base real.
- `app/db/seed.py` solo siembra Roles + usuario admin porque EstadoPedido y
  FormaPago pertenecen a módulos que todavía no existen (productos, pedidos).
