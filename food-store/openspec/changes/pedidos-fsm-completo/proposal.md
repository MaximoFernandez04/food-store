## Why

Se fusionan `pedidos-atomic-create`, `pedidos-fsm` y `pedidos-cancel` (3
changes separados en `docs/CHANGES.md`) en uno solo: comparten el mismo
agregado (Pedido) y la FSM es indisociable de la creación y la
cancelación — separarlos en 3 changes habría significado tocar
`service.py` tres veces sin beneficio real, con el tiempo acotado que queda.

## What Changes

- `app/modules/pedidos/`: EstadoPedido y FormaPago (catálogos),
  Pedido, DetallePedido (snapshot), HistorialEstadoPedido (append-only)
- Creación atómica de pedido: valida stock con lock de fila
  (`SELECT FOR UPDATE`, RN-PE04), snapshot de precio/nombre/dirección,
  todo-o-nada (RN-PE05)
- FSM de 6 estados con las reglas de Historias_de_Usuario.txt (más
  detalladas que la tabla simplificada del PDF):
  - El stock se descuenta al CONFIRMAR (no al crear) y se restaura al
    cancelar desde cualquier estado donde ya estaba descontado
  - PENDIENTE → CONFIRMADO es EXCLUSIVAMENTE automática (la ejecuta
    `confirmar_por_pago()`, que va a llamar el módulo de pagos — ningún
    router de pedidos la expone)
  - Permisos de cancelación distintos según el estado de origen
    (RN-FS08, RN-RB08)
- `app/db/seed.py` completo: ya no quedan los TODO de EstadoPedido/FormaPago

## Impact

- Depende de `productos` (stock, precio) y `direcciones` (snapshot de
  dirección), ya aplicados
- Desbloquea `pagos-mercadopago` (que va a llamar a `confirmar_por_pago()`)
  y `admin-dashboard` (que va a leer `Pedido`/`HistorialEstadoPedido`)
- Decisión de diseño: `FormaPago` vive en `pedidos/model.py`, no en
  `productos/`, porque solo lo usa Pedido (evita una dependencia cruzada
  innecesaria entre productos y pedidos)
- Sin tests automatizados todavía (validado manualmente, ver tasks.md)
