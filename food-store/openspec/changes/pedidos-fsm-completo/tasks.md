## 1. Modelos

- [x] 1.1 EstadoPedido (catálogo, orden, es_terminal)
- [x] 1.2 FormaPago (catálogo, habilitado)
- [x] 1.3 Pedido (snapshot de dirección como texto, NUMERIC para montos)
- [x] 1.4 DetallePedido (snapshot nombre/precio, `personalizacion INTEGER[]`)
- [x] 1.5 HistorialEstadoPedido (append-only, estado_desde nullable)

## 2. Repositorios

- [x] 2.1 `PedidoRepository.get_by_id_for_update` (lock de fila)
- [x] 2.2 `ProductoRepository.get_by_id_for_update` (lock de fila, sumado en este change)
- [x] 2.3 `PedidoRepository.search` (filtro por usuario/estado + paginación)
- [x] 2.4 `DetallePedidoRepository`, `HistorialRepository`, `EstadoPedidoRepository`, `FormaPagoRepository`

## 3. Service — Creación

- [x] 3.1 Valida dirección propia (si no es retiro en local) y forma de pago habilitada
- [x] 3.2 Por cada item: lock de fila sobre Producto, valida disponible + stock suficiente (todo o nada)
- [x] 3.3 Valida que la personalización sea un subconjunto de los ingredientes reales del producto
- [x] 3.4 Snapshot de nombre/precio en cada DetallePedido
- [x] 3.5 Primer registro de HistorialEstadoPedido con estado_desde=None

## 4. Service — FSM

- [x] 4.1 Mapa de transiciones válidas (6 estados, 2 terminales)
- [x] 4.2 Bloqueo explícito de PENDIENTE→CONFIRMADO manual (RN-FS02)
- [x] 4.3 `confirmar_por_pago()`: descuenta stock atómicamente, idempotente si ya estaba CONFIRMADO
- [x] 4.4 Permisos de cancelación por estado de origen (PENDIENTE: propietario/PEDIDOS/ADMIN; CONFIRMADO: PEDIDOS/ADMIN; EN_PREPARACION: solo ADMIN)
- [x] 4.5 Restaurar stock al cancelar desde CONFIRMADO o EN_PREPARACION (no desde PENDIENTE)
- [x] 4.6 motivo obligatorio al cancelar

## 5. Router

- [x] 5.1 GET /api/v1/pedidos (propios o todos según rol, filtro por estado, paginación)
- [x] 5.2 GET /api/v1/pedidos/{id} (con ownership check)
- [x] 5.3 POST /api/v1/pedidos
- [x] 5.4 PATCH /api/v1/pedidos/{id}/estado
- [x] 5.5 GET /api/v1/pedidos/{id}/historial

## 6. Seed

- [x] 6.1 6 EstadoPedido (PENDIENTE...CANCELADO, con es_terminal correcto)
- [x] 6.2 3 FormaPago (MERCADOPAGO, EFECTIVO, TRANSFERENCIA)

## 7. Validación manual (PostgreSQL real esta vez, no SQLite — `personalizacion INTEGER[]` y `SELECT FOR UPDATE` no existen en SQLite)

- [x] 7.1 Crear pedido: stock NO se descuenta todavía
- [x] 7.2 Intentar confirmar manualmente (ADMIN) → 403 MANUAL_CONFIRM_FORBIDDEN
- [x] 7.3 `confirmar_por_pago()` (simulando el webhook) → stock SÍ se descuenta
- [x] 7.4 CLIENT intenta avanzar estado → 403
- [x] 7.5 ADMIN avanza CONFIRMADO→EN_PREPARACION → 200
- [x] 7.6 CLIENT intenta cancelar EN_PREPARACION → 403 (RN-RB08)
- [x] 7.7 ADMIN cancela desde EN_PREPARACION → stock se restaura completo
- [x] 7.8 Cancelar directo desde CONFIRMADO → stock también se restaura
- [x] 7.9 Cancelar desde PENDIENTE → stock NO se toca (nunca se descontó)
- [x] 7.10 Historial completo queda registrado en orden, append-only
- [ ] 7.11 Tests automatizados (pytest) — pendiente, Epic 11
