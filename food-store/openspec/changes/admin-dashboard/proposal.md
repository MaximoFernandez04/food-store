## Why

Última pieza de backend que faltaba para que el panel de admin del
frontend tenga de dónde leer sus KPIs. Sin esto, el módulo `usuarios` no
tenía ningún router propio (solo se usaba internamente desde `auth`) y
no había ningún endpoint de métricas agregadas.

## What Changes

- `GET /api/v1/admin/dashboard`: total de ventas (excluye CANCELADO),
  conteo de pedidos por estado, top 5 productos más vendidos, total de
  usuarios y productos activos
- Es de solo lectura sobre tablas que ya existen (Pedido, DetallePedido,
  Usuario, Producto) — no se creó modelo ni tabla nueva, así que se
  consulta directo vía `uow.session` en el service en vez de sumar una
  capa de repository para un único endpoint
- Restringido a rol ADMIN (RBAC: ni STOCK ni PEDIDOS tienen acceso a
  datos financieros según la tabla de roles de la sección 4.2)
- Se aprovechó para sumar `categorias_de()`/`quitar_categoria()` al
  repository de productos y permitir editar `categoria_ids`,
  `ingrediente_ids`, `stock_cantidad` y `disponible` en un solo
  `PUT /productos/{id}` — lo necesitaba el form de edición del admin del
  frontend para no tener que hacer 4 requests separadas por cada edición

## Impact

- Depende de `pedidos-fsm-completo` y `pagos-mercadopago` (lee sus tablas)
- No agrega tablas ni migraciones nuevas
- **Deliberadamente NO se expone gestión de usuarios/roles desde el
  admin** (CRUD usuarios + asignación de roles del módulo `usuarios`
  original del roadmap) por el tiempo disponible — la rúbrica de "Panel
  Admin" no lo pide explícitamente (pide dashboard + CRUD
  categorías/productos + gestión de pedidos + stock, los 4 ya cubiertos)
