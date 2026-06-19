## Why

Con menos de 2 días hasta la entrega, se construyó el frontend completo
de una sola vez en vez de ir feature por feature como se hizo con el
backend — el costo de integración de un frontend nuevo es mucho menor
que el de migraciones de base de datos (es solo copiar una carpeta,
`npm install`, listo), así que no tenía sentido fragmentar la entrega en
6-7 rondas de ida y vuelta. Fusiona lo que en `docs/CHANGES.md` eran los
Epic02 a Epic10 del roadmap original.

## What Changes

- **Setup**: Vite + React 18 + TS 5 + Tailwind, `strict: true`, sin `any`
- **Stores (Zustand, los 4 de la spec)**: `authStore` (persist solo
  accessToken), `cartStore` (persist items completos), `paymentStore`
  (sin persist), `uiStore` (sin persist)
- **API + hooks (TanStack Query)**: un módulo por dominio bajo `api/` y
  `hooks/`, con interceptor de Axios que refresca el access token ante
  401 automáticamente (con promesa compartida entre requests concurrentes)
- **Catálogo**: grilla con buscador debounced, filtro por categoría,
  paginación, modal de personalización (sacar ingredientes removibles)
- **Carrito**: drawer persistente, edición de cantidades
- **Checkout**: selección de dirección (o retiro en local), forma de
  pago, y el Brick `CardPayment` de `@mercadopago/sdk-react` para
  MERCADOPAGO. Para EFECTIVO/TRANSFERENCIA el pedido queda PENDIENTE
  hasta que el staff lo confirme manualmente desde el panel
- **Seguimiento de pedidos**: timeline de historial con polling de 30s
  que se detiene al llegar a un estado terminal
- **Panel admin**: dashboard con recharts, CRUD de categorías y
  productos (con categorías/ingredientes asociados), gestión de stock y
  disponibilidad inline, gestión de pedidos con los botones de avance de
  la FSM
- **Diseño**: paleta propia (mostaza/oliva/brasa sobre fondo papel),
  Fraunces + Inter + JetBrains Mono, timeline de pedido con motivo
  perforado tipo ticket de cocina como elemento de firma

## Impact

- Depende de absolutamente todo el backend (auth, catálogo, pedidos,
  pagos, admin)
- **Encontrado y corregido en el camino**: la FSM de pedidos bloqueaba
  `PENDIENTE → CONFIRMADO` de forma manual sin excepciones — correcto
  para MERCADOPAGO (donde el webhook confirma), pero dejaba sin forma de
  confirmarse nunca a un pedido pagado en EFECTIVO o TRANSFERENCIA. Se
  relajó la regla solo para esos dos casos (ver `pedidos-fsm-completo`)
- **Deuda conocida, aceptada por tiempo**:
  - Sin tests automatizados (ni backend ni frontend)
  - Sin gestión de usuarios/roles desde el admin
  - Validación de errores de TanStack Form básica (no exhaustiva por campo)
  - El motivo de cancelación en el panel admin usa `window.prompt()` en
    vez de un modal propio
  - No se verificó visualmente en un navegador real (sandbox sin acceso
    a la red del usuario) — se validó con `tsc -b`, `vite build` y
    `eslint` limpios, más revisión manual de cada pantalla contra los
    schemas reales del backend
