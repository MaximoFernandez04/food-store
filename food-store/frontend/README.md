# Food Store — Frontend

React + TypeScript + Vite + Tailwind + Zustand + TanStack Query.

## Setup

```bash
npm install
cp .env.example .env   # completar VITE_MP_PUBLIC_KEY con tu Public Key de MercadoPago
npm run dev
```

Por defecto corre en `http://localhost:5173` — coincide con el
`CORS_ORIGINS` default del backend, así que no hace falta tocar nada ahí.

El backend tiene que estar corriendo en `http://localhost:8000` (o lo
que pongas en `VITE_API_URL`).

## Scripts

- `npm run dev` — servidor de desarrollo
- `npm run build` — `tsc -b && vite build`, deja todo en `dist/`
- `npm run lint` — eslint

## Estructura (Feature-Sliced Design)

```
src/
  types/        tipos compartidos (espejo de los schemas Pydantic)
  api/           un módulo por dominio, llama al backend con axios
  hooks/         TanStack Query sobre cada api/
  store/         los 4 stores de Zustand (auth, cart, payment, ui)
  components/    primitivas reutilizables (Button, Input, Modal, ...)
  features/      lógica de cada feature (auth, catalogo, cart, checkout,
                  direcciones, pedidos, admin)
  pages/         wrappers finos que conectan rutas a features/
```

## Notas

- `authStore` solo persiste el `accessToken` en localStorage (vía
  `persist` de Zustand). Al recargar la página, `App.tsx` llama a
  `GET /auth/me` para reconstruir el usuario — si el access token ya
  venció y no hay refresh token en memoria (se perdió al recargar),
  fuerza un nuevo login. Es una limitación conocida y documentada.
- El pago con tarjeta usa el Brick `CardPayment` de
  `@mercadopago/sdk-react`. Los datos de la tarjeta nunca tocan este
  frontend ni el backend — se tokenizan directo contra MercadoPago.
