## Why

Con el tiempo acotado que queda, se fusionan en un solo change los 4
changes que `docs/CHANGES.md` listaba por separado (`categorias-create`,
`ingredientes-crud`, `productos-create-edit` + sus 5 sub-changes,
`direcciones-crud`), porque son CRUDs independientes entre sí que siguen
el mismo patrón ya validado en `auth-register-login-refresh` y no
ameritan 4 documentos de diseño separados.

## What Changes

- `app/modules/categorias/`: jerarquía recursiva (CTE), soft delete con
  validación (no se puede borrar si tiene subcategorías activas)
- `app/modules/productos/`: Producto, Ingrediente, ProductoCategoria
  (M:N + es_principal), ProductoIngrediente (M:N + es_removible).
  Listado con filtros (categoria/disponible/search) + paginación.
  Endpoints separados para disponibilidad y stock (PATCH idempotentes)
- `app/modules/direcciones/`: CRUD + regla "solo una principal por
  usuario" (al marcar una nueva, se desmarca la anterior)
- `UnitOfWork` actualizado con los 4 repositorios nuevos
- `main.py` y `alembic/env.py` actualizados con los routers/modelos nuevos

## Impact

- Depende de `backend-core-setup` (aplicado) y de `usuarios` (vía
  `direcciones` → FK a `usuario.id`)
- Desbloquea `pedidos-atomic-create` (necesita Producto + DireccionEntrega)
- Sin tests automatizados (validado manualmente, ver tasks.md) — se
  decidió no escribir pytest todavía por el tiempo acotado; queda
  documentado como deuda en Epic 11
