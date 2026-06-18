## Why

Último módulo del dominio "Ventas, Pagos y Trazabilidad". Sin esto, la
FSM de pedidos nunca sale de PENDIENTE en un flujo real, porque
`confirmar_por_pago()` (agregado en `pedidos-fsm-completo`) necesita
quién la llame.

## What Changes

- `app/modules/pagos/`: modelo `Pago` (1:N con Pedido — RN-PA08, un
  pedido puede tener varios intentos de pago si el primero es rechazado)
- `mp_client.py`: wrapper delgado sobre el SDK oficial `mercadopago`
  (pinneado a 3.2.0 — verificado contra la versión real instalada, no
  asumido). Aislado en su propio módulo para poder mockear en tests sin
  pegarle a la red real de MercadoPago.
- `POST /api/v1/pagos/crear`: tokeniza vía MercadoPago.js en el frontend
  (los datos de tarjeta nunca llegan a este backend, PCI SAQ-A), idempotency_key
  UUID por intento (RN-PA02)
- `POST /api/v1/pagos/webhook`: endpoint público (sin auth) para la
  notificación IPN. Re-consulta el pago contra la API de MP en vez de
  confiar en el payload de la notificación (RN-PA04) y SIEMPRE responde
  200 así MP no reintenta indefinidamente (RN-PA03)
- `GET /api/v1/pagos/{pedido_id}`: último pago de un pedido

## Impact

- Depende de `pedidos-fsm-completo` (llama a `confirmar_por_pago()`)
- **Deuda conocida, aceptada por tiempo**: no se valida la firma
  (`x-signature`) del webhook contra el secret de la app de MP. En este
  TPI el webhook no es alcanzable desde internet real sin ngrok, así que
  el riesgo práctico es bajo, pero en producción real esto es obligatorio
- Probado con Postgres real (no SQLite) mockeando `mp_client.crear_pago_mp`
  / `mp_client.consultar_pago_mp` — no hay acceso de red a la API real de
  MercadoPago desde el entorno de testing
- Pendiente del lado del usuario: conseguir credenciales TEST reales en
  https://www.mercadopago.com.ar/developers/panel/app y, para probar el
  webhook con la API real (no mockeada), expone localhost con `ngrok http 8000`
