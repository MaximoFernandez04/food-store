## 1. Categorías

- [x] 1.1 Modelo Categoria (self-FK, soft delete)
- [x] 1.2 Repositorio con CTE recursiva (`arbol_completo`)
- [x] 1.3 Service: valida padre existente, soft-delete bloqueado si tiene hijos
- [x] 1.4 Router: GET (lista, árbol, detalle), POST/PUT/DELETE (solo ADMIN)

## 2. Ingredientes + Productos

- [x] 2.1 Modelos Producto, Ingrediente, ProductoCategoria, ProductoIngrediente
- [x] 2.2 Repositorio Producto: búsqueda con filtros + paginación real
- [x] 2.3 Service: valida nombre único, categorías/ingredientes existentes
- [x] 2.4 Router productos: CRUD + PATCH disponibilidad + PATCH stock
      (ADMIN/STOCK) + sub-rutas de ingredientes del producto
- [x] 2.5 Router ingredientes: CRUD básico (ADMIN)

## 3. Direcciones

- [x] 3.1 Modelo DireccionEntrega
- [x] 3.2 Repositorio con `unset_principal`
- [x] 3.3 Service: solo una dirección principal por usuario
- [x] 3.4 Router: CRUD propio (CLIENT autenticado) + PATCH /principal

## 4. Integración

- [x] 4.1 UnitOfWork con los 4 repos nuevos
- [x] 4.2 main.py registra los 4 routers nuevos
- [x] 4.3 alembic/env.py conoce los modelos nuevos

## 5. Validación manual (SQLite, sin Postgres disponible en este entorno)

- [x] 5.1 Crear categoría + subcategoría → árbol con `depth` correcto
- [x] 5.2 Crear producto con categoría e ingrediente asociados
- [x] 5.3 Filtrar productos por categoría → devuelve solo los esperados
- [x] 5.4 Actualizar stock vía PATCH
- [x] 5.5 Crear 2 direcciones, marcar la 2da como principal → la 1ra se
      desmarca sola
- [x] 5.6 Un usuario CLIENT intenta crear una categoría → 403
- [ ] 5.7 Repetir contra PostgreSQL real antes de archivar
- [ ] 5.8 Tests automatizados (pytest) — pendiente, Epic 11
