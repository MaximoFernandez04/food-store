## 1. Endpoint

- [x] 1.1 Agregaciones: total_ventas, pedidos_por_estado (6 estados, siempre completos aunque tengan 0), top 5 productos
- [x] 1.2 Restricción a rol ADMIN

## 2. Productos — soporte para el form de edición del admin

- [x] 2.1 `categorias_de()` / `quitar_categoria()` en el repository (faltaba la simétrica de `asignar_categoria`)
- [x] 2.2 `ProductoUpdate` acepta `stock_cantidad`, `disponible`, `categoria_ids`, `ingrediente_ids` además de los campos que ya tenía
- [x] 2.3 `categoria_ids`/`ingrediente_ids` en el update son reemplazo completo del set, no merge incremental
- [x] 2.4 `ProductoDetail` ahora incluye `categorias` (antes solo tenía `ingredientes`)

## 3. Validación manual (Postgres real)

- [x] 3.1 ADMIN ve el dashboard con datos reales tras crear/confirmar pedidos
- [x] 3.2 CLIENT no puede ver el dashboard (403)
- [x] 3.3 Editar categorias_ids de un producto reemplaza el set completo correctamente
- [ ] 3.4 Tests automatizados (pytest) — pendiente, Epic 11
