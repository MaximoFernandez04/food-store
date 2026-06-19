## 1. Setup

- [x] 1.1 Vite + React 18 + TS 5 + Tailwind, tokens de diseño propios
- [x] 1.2 `strict: true`, cero `any`
- [x] 1.3 Axios con interceptor de refresh automático ante 401

## 2. Estado global

- [x] 2.1 `authStore` (persist solo accessToken; refreshToken en memoria)
- [x] 2.2 `cartStore` (persist items completos, merge por producto+personalización)
- [x] 2.3 `paymentStore` (sin persist, estado del Brick de MP)
- [x] 2.4 `uiStore` (sin persist; drawer del carrito, modal de confirmación global)

## 3. Catálogo y carrito

- [x] 3.1 Grilla con buscador (debounce 350ms), filtro por categoría, paginación
- [x] 3.2 Modal de personalización (ingredientes removibles, cantidad)
- [x] 3.3 Carrito: drawer, edición de cantidad, subtotal/envío/total

## 4. Checkout y pagos

- [x] 4.1 Selección de dirección (o retiro en local) y forma de pago
- [x] 4.2 Brick `CardPayment` para MERCADOPAGO
- [x] 4.3 Flujo directo a PENDIENTE para EFECTIVO/TRANSFERENCIA
- [x] 4.4 Reintento de pago desde el detalle del pedido si quedó PENDIENTE

## 5. Pedidos (cliente)

- [x] 5.1 Listado con paginación y badge de estado
- [x] 5.2 Detalle con timeline de historial (polling 30s, se detiene en estado terminal)
- [x] 5.3 Cancelación con confirmación

## 6. Panel admin

- [x] 6.1 Dashboard: KPIs + gráfico de pedidos por estado + top 5 productos
- [x] 6.2 CRUD de categorías (con padre opcional)
- [x] 6.3 CRUD de productos (categorías/ingredientes asociados, stock y disponibilidad inline)
- [x] 6.4 Gestión de pedidos: filtro por estado, botones de avance de la FSM, cancelación

## 7. Validación

- [x] 7.1 `npx tsc -b` sin errores
- [x] 7.2 `npm run build` sin errores
- [x] 7.3 `eslint` sin errores (1 warning inofensivo)
- [ ] 7.4 Verificación visual en navegador real — pendiente, hacerla apenas se integre localmente
- [ ] 7.5 Tests E2E / componentes — pendiente, Epic 11
