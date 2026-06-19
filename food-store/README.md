Integrantes: Alex Rodríguez, Ignacio Bevilacqua, Máximo Fernández

# 🍔 Food Store

Sistema de gestión de pedidos de comida — Trabajo Práctico Integrador,
Gestion de Desarrollo de Software. Stack: **FastAPI + SQLModel + PostgreSQL** (backend) y
**React + TypeScript + Vite** (frontend), con pagos integrados vía
**MercadoPago**.

## Demo

- Video: https://youtu.be/Dmzotj8XaYU
- Repo: https://github.com/MaximoFernandez04/food-store.git

## Stack

| Capa | Tecnología |
|---|---|
| Backend | FastAPI, SQLModel, PostgreSQL 15+, Alembic, Passlib (bcrypt), slowapi, SDK MercadoPago |
| Frontend | React 18, TypeScript, Vite, Tailwind, Zustand, TanStack Query, TanStack Form, recharts, `@mercadopago/sdk-react` |
| Arquitectura backend | Router → Service → Unit of Work → Repository → Model, por feature |
| Arquitectura frontend | Feature-Sliced Design |

## Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ corriendo localmente (con [pgAdmin](https://www.pgadmin.org/) o el cliente `psql` para crear la base)
- Una cuenta de developer de MercadoPago (gratis) para las credenciales de test

## 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# completar DATABASE_URL, SECRET_KEY, MP_ACCESS_TOKEN y MP_PUBLIC_KEY en .env
```

Crear la base de datos vacía (el nombre tiene que coincidir con `DATABASE_URL`).
Si tenés `psql` en el PATH:

```bash
psql -U postgres -c "CREATE DATABASE foodstore_db;"
```

Si no (frecuente en Windows, el instalador de Postgres no siempre lo
agrega al PATH), hacelo desde **pgAdmin**: conectate al servidor → click
derecho en **Databases** → **Create** → **Database...** → nombre
`foodstore_db`.

```bash
alembic upgrade head
python -m app.db.seed

uvicorn app.main:app --reload
```

Backend en `http://localhost:8000`. Documentación interactiva en
`http://localhost:8000/docs` (Swagger) y `/redoc`.

### Variables de entorno del backend

Ver `.env.example` para la lista completa. Las más importantes:

| Variable | Para qué |
|---|---|
| `DATABASE_URL` | conexión a PostgreSQL |
| `SECRET_KEY` | firma de los JWT (mínimo 32 caracteres) |
| `MP_ACCESS_TOKEN` | credencial **privada** de MercadoPago, solo backend |
| `MP_PUBLIC_KEY` | credencial pública de MercadoPago (se repite en el frontend) |
| `CORS_ORIGINS` | por defecto `["http://localhost:5173"]`, ya coincide con el puerto default de Vite |

Las credenciales de MercadoPago (`TEST-...`) se generan gratis en el
[panel de developers de MercadoPago](https://www.mercadopago.com.ar/developers/panel/app),
creando una aplicación de prueba (solución: **Pagos online** → **Checkout API**, sin plataforma de ecommerce).

## 2. Frontend

```bash
cd frontend
npm install

cp .env.example .env
# VITE_API_URL=http://localhost:8000
# VITE_MP_PUBLIC_KEY=la misma Public Key que pusiste en el backend

npm run dev
```

Frontend en `http://localhost:5173`.

## 3. Usuario administrador (seed)

El script de seed crea un usuario ADMIN para entrar directo al panel:

```
email:    admin@foodstore.com
password: Admin1234!
```

**Cambiar esta contraseña antes de cualquier uso real** — el seed la deja así a propósito para que la corrección pueda entrar sin pedirte nada.

El catálogo arranca vacío a propósito (el seed solo carga roles, estados
de pedido, formas de pago y este usuario) — cargá categorías y productos
desde **Panel → Categorías / Productos** una vez logueado como admin.

## 4. Probar un pago con MercadoPago (sandbox)

Con el backend y el frontend corriendo: agregá algo al carrito → checkout
→ "Tarjeta (MercadoPago)". En el sandbox, **el resultado del pago lo
decide el nombre del titular que pongas, no la tarjeta**:

| Resultado | Número de tarjeta | Vencimiento | CVV | Titular | DNI |
|---|---|---|---|---|---|
| Pago aprobado | 4509 9535 6623 3704 (Visa) | 11/30 | 123 | `APRO` | 12345678 |
| Rechazado (error general) | 4509 9535 6623 3704 (Visa) | 11/30 | 123 | `OTHE` | 12345678 |
| Pendiente | 4509 9535 6623 3704 (Visa) | 11/30 | 123 | `CONT` | — |

(Lista completa de códigos en la [documentación oficial](https://www.mercadopago.com.ar/developers/es/docs/your-integrations/test/cards) — cambia de tanto en tanto, conviene chequearla si algo no da el resultado esperado.)

Si el pago se aprueba, el pedido pasa a `CONFIRMADO` automáticamente. Para
que el **webhook** de MercadoPago le llegue a tu backend en `localhost`
(confirmación 100% async, no por la respuesta directa del POST), necesitás
exponerlo con algo como [ngrok](https://ngrok.com/) y configurar esa URL
pública como `MP_NOTIFICATION_URL`. Sin eso, el pago se procesa igual y
el resultado se ve por la respuesta directa de `POST /pagos/crear` — la
única diferencia es que la confirmación automática *por webhook* no se
dispara en local.

## 5. Estructura del repo

```
food-store/
  backend/    FastAPI
  frontend/   React
  openspec/   documentación de cada feature (proposal + tasks) siguiendo SDD
```

## 6. Roles y permisos

| Rol | Puede |
|---|---|
| ADMIN | todo |
| STOCK | ver productos, actualizar stock y disponibilidad |
| PEDIDOS | ver y avanzar el estado de los pedidos |
| CLIENT | catálogo, carrito, sus propios pedidos |

## 7. Limitaciones conocidas

- No hay tests automatizados (pytest ni de frontend) — quedó fuera por
  tiempo, no por desconocimiento de cómo escribirlos.
- El panel admin no tiene gestión de usuarios/roles (sí tiene categorías,
  productos, stock y pedidos).
- No se valida la firma/HMAC del webhook de MercadoPago — en producción
  real haría falta.
- El motivo de cancelación en el panel admin se pide con un
  `window.prompt()` en vez de un modal propio.
