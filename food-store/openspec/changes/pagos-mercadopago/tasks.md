## 1. Modelo y repositorio

- [x] 1.1 `Pago` (mp_payment_id nullable+unique, idempotency_key unique, external_reference)
- [x] 1.2 `get_by_idempotency_key`, `get_by_mp_payment_id`, `list_by_pedido`, `get_ultimo_de_pedido`

## 2. Cliente MercadoPago

- [x] 2.1 `mp_client.py` aislado (permite mockear en tests)
- [x] 2.2 Verificar API real del SDK instalado (`mercadopago.config.RequestOptions`, `custom_headers`) — no asumir
- [x] 2.3 Pinnear versión exacta en requirements.txt

## 3. Service

- [x] 3.1 `crear_pago`: valida ownership + estado PENDIENTE del pedido
- [x] 3.2 idempotency_key UUID por intento (no por pedido)
- [x] 3.3 Si `status == "approved"` al crear → confirma el pedido en el mismo flujo (sin esperar el webhook)
- [x] 3.4 `procesar_webhook`: re-consulta contra la API (RN-PA04), nunca confía en el payload
- [x] 3.5 Idempotente ante notificaciones duplicadas (mismo status → no-op)
- [x] 3.6 Caso borde: webhook llega antes que el Pago exista en BD → lo crea por `external_reference`

## 4. Router

- [x] 4.1 POST /api/v1/pagos/crear (autenticado)
- [x] 4.2 POST /api/v1/pagos/webhook (público, siempre devuelve 200, errores van a traceback/log)
- [x] 4.3 GET /api/v1/pagos/{pedido_id} (propietario o ADMIN/PEDIDOS)

## 5. Integración

- [x] 5.1 `uow.py`: `PagoRepository`
- [x] 5.2 `main.py`: router + modelo
- [x] 5.3 `alembic/env.py`: modelo

## 6. Validación manual (Postgres real, mockeando mp_client)

- [x] 6.1 Pago aprobado al crear → pedido CONFIRMADO automático, stock descontado
- [x] 6.2 Pago rechazado → pedido sigue PENDIENTE
- [x] 6.3 Pago pending → luego webhook con status approved → pedido CONFIRMADO
- [x] 6.4 Webhook duplicado (mismo status) → no rompe, no duplica
- [x] 6.5 Webhook cuando `consultar_pago_mp` lanza excepción → sigue respondiendo 200
- [x] 6.6 No se puede pagar un pedido que ya no está PENDIENTE
- [x] 6.7 GET pago de un pedido
- [ ] 6.8 Prueba con API real de MercadoPago + ngrok — pendiente de credenciales TEST del usuario
- [ ] 6.9 Validación de firma del webhook (`x-signature`) — deuda conocida, no implementada
- [ ] 6.10 Tests automatizados (pytest) — pendiente, Epic 11
