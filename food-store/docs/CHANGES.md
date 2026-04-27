# Food Store — Mapa Maestro de Changes (OPSX / SDD / Feature-First)

> 🚦 Este archivo organiza TODO el desarrollo del sistema Food Store en changes atómicos y secuenciales. Seguí este roadmap: cada change incluye nombre sugerido (kebab-case), funcionalidad cubierta, historias de usuario principales y dependencias con otros changes (si existen).
> 
> **REGLAS:**
> - Cada change debe tener sus artefactos OPSX (`proposal.md`, `design.md`, `tasks.md`)
> - No avances al siguiente change si depende de uno aún incompleto
> - Proponé cambios fusionados/split según experiencia real, pero TODO debe quedar justificado acá

---

## Epic 00 — Infraestructura y Setup Inicial

| Change Name                   | Funcionalidad / Scope                                      | User Stories Principales | Depende de           |
|------------------------------|------------------------------------------------------------|-------------------------|----------------------|
| init-repo-structure          | Monorepo, carpetas /backend y /frontend, .gitignore, README | US-000                  | —                    |
| backend-core-setup           | FastAPI, SQLModel, Alembic, config env, middlewares         | US-000a                 | init-repo-structure  |
| backend-db-migrations        | Migraciones Alembic full, datos seed, fixtures              | US-000b                 | backend-core-setup   |
| frontend-core-setup          | React (TS), Vite, setup Axios, routing, estilo base, env    | US-000c                 | init-repo-structure  |
| common-infra-patterns        | BaseRepository, Unit of Work, get_current_user, roles dep.  | US-000d                 | backend-db-migrations|
| frontend-stores-zustand      | Configuración de 4 stores: auth, cart, ui, payment          | US-000e                 | frontend-core-setup  |

---

## Epic 01 — Autenticación, Autorización, Seguridad

| Change Name                  | Funcionalidad / Scope                                    | User Stories           | Depende de             |
|-----------------------------|----------------------------------------------------------|------------------------|------------------------|
| auth-register-login-refresh  | Registro, login, refresh, bcrypt hash, RBAC, rate limit  | US-001, US-002, US-003 | common-infra-patterns   |
| auth-logout                 | Logout + invalidación de refresh token                   | US-004                | auth-register-login-refresh |
| rbac-role-management        | Asignación/verificación roles, require_role, guards       | US-005, US-006        | auth-register-login-refresh |
| security-rate-limiting      | Límite de intentos en login y endpoints críticos          | US-073                | auth-register-login-refresh |
| global-backend-errors       | Manejo errores (RFC7807, validation, forbidden)           | US-068                | auth-register-login-refresh |
| input-sanitization          | Validación/sanitización, protección XSS/SQLi              | US-074                | auth-register-login-refresh |

---

## Epic 02 — Navegación y Feature Slicing FE

| Change Name                  | Funcionalidad / Scope                                   | User Stories           | Depende de                  |
|-----------------------------|---------------------------------------------------------|------------------------|-----------------------------|
| menu-por-rol                | Sidebar/nav dependiente de rol (CLIENT/STOCK/PEDIDOS/ADMIN) | US-075              | rbac-role-management         |
| fe-route-guards             | Protege rutas según auth y rol (frontend)                | US-076                | menu-por-rol                |
| token-autorefresh-fe        | Renovación automática de sesion en FE, 401 → refresh     | US-066                | fe-route-guards, auth-register-login-refresh |
| global-error-handler-fe     | Mapeo y visualización de errores (toasts, 404/403/500)   | US-067                | fe-route-guards              |

---

## Epic 03 — Categorías

| Change Name                  | Funcionalidad / Scope                                      | User Stories       | Depende de             |
|-----------------------------|------------------------------------------------------------|--------------------|------------------------|
| categorias-create           | CRUD categorías (jerarquía, FK padre)                      | US-007, US-008, US-009 | rbac-role-management   |
| categorias-soft-delete      | Eliminación lógica, protección CK y referencial            | US-010                 | categorias-create      |

---

## Epic 04 — Ingredientes y Alérgenos

| Change Name                  | Funcionalidad / Scope                                    | User Stories      | Depende de          |
|-----------------------------|----------------------------------------------------------|-------------------|---------------------|
| ingredientes-crud           | CRUD ingredientes con flag esAlergeno + soft delete      | US-011 a US-014   | rbac-role-management|

---

## Epic 05 — Productos y Catálogo

| Change Name                  | Funcionalidad / Scope                         | User Stories           | Depende de               |
|-----------------------------|-----------------------------------------------|------------------------|--------------------------|
| productos-create-edit       | Alta/edit producto, precio fijo/stock/img      | US-015, US-020        | categorias-create, ingredientes-crud |
| productos-asignar-categorias| Producto x Categoría (M2M)                     | US-016                | productos-create-edit    |
| productos-asignar-ingredientes| Producto x Ingrediente (M2M)                  | US-017                | productos-create-edit, ingredientes-crud |
| productos-listar-buscar     | FQDN público: listar + filtros, paginación     | US-018                | productos-create-edit    |
| productos-view-detail       | Detalle con ingredientes/alérgenos             | US-019, US-024        | productos-asignar-ingredientes |
| productos-stock             | Gestión de stock (patch, atomic update)        | US-021                | productos-create-edit    |
| productos-soft-delete       | Baja lógica producto, histórico en pedidos     | US-022                | productos-create-edit    |
| productos-filtrar-alergenos | Filtros de exclusión por ingredientes          | US-023                | productos-view-detail    |

---

## Epic 06 — Direcciones de Entrega

| Change Name                  | Funcionalidad / Scope                               | User Stories           | Depende de    |
|-----------------------------|-----------------------------------------------------|------------------------|---------------|
| direcciones-crud            | CRUD direcciones + predeterminada x user            | US-024 a US-028        | rbac-role-management |

---

## Epic 07 — Carrito (Client-side)

| Change Name                  | Funcionalidad / Scope                          | User Stories             | Depende de                |
|-----------------------------|-----------------------------------------------|--------------------------|---------------------------|
| cart-client-persist          | Carrito Zustand/localStorage: crear, actualizar, persistir | US-029 a US-034    | frontend-stores-zustand   |
| cart-personalizacion         | Exclusión ingredientes en carrito (array IDs)           | US-035                | productos-asignar-ingredientes |

---

## Epic 08 — Pedidos FSM & Trazabilidad

| Change Name                  | Funcionalidad / Scope                         | User Stories                | Depende de                     |
|-----------------------------|-----------------------------------------------|-----------------------------|--------------------------------|
| pedidos-atomic-create        | Crear pedido atómico + snapshot precio + dirección | US-035 a US-038        | cart-client-persist, direcciones-crud |
| pedidos-view-own-list        | Cliente ve sus pedidos, ADMIN//PEDIDOS ven todos   | US-049, US-061          | pedidos-atomic-create          |
| pedidos-fsm                  | Máquina de estados (FSM), historial append-only, validaciones | US-039 a US-044 | pedidos-atomic-create          |
| pedidos-cancel               | Cancelación propia o por Admin/Gestor FE/BE       | US-043                  | pedidos-fsm                   |

---

## Epic 09 — Pagos MercadoPago

| Change Name                  | Funcionalidad / Scope                        | User Stories          | Depende de           |
|-----------------------------|----------------------------------------------|-----------------------|----------------------|
| pagos-mercadopago           | Integración checkout API, idempotency key    | US-045, US-046        | pedidos-atomic-create |
| pagos-webhook-ipn           | Webhook IPN - transición automática FSM      | US-046                | pagos-mercadopago    |
| pagos-multitries-historial  | Múltiples intentos de pago por pedido        | US-048                | pagos-mercadopago    |

---

## Epic 10 — Panel Admin y Métricas

| Change Name                  | Funcionalidad / Scope                         | User Stories         | Depende de                   |
|-----------------------------|-----------------------------------------------|----------------------|------------------------------|
| admin-dashboard              | Dashboard KPIs, gráficas, panel de gestión    | US-059, US-060        | productos-create-edit, pedidos-fsm |
| admin-gestionar-usuarios     | CRUD usuarios y roles desde panel             | US-005b, US-054      | rbac-role-management         |
| admin-gestionar-stock        | Gestión avanzada stock por Admin              | US-021b              | productos-stock              |

---

## Epic 11 — Cross-cutting: Validaciones, Tests e Integridad

| Change Name                  | Funcionalidad / Scope                           | User Stories            | Depende de         |
|-----------------------------|-------------------------------------------------|-------------------------|--------------------|
| tests-pytest-coverage        | Tests unitarios + cobertura >60%                | Bonus                  | Todos los backends |
| tests-e2e-frontend           | Tests end to end, mínimos críticos              | Bonus                  | Todo frontend      |
| deploy-cloud-readme          | Deploy en Railway/Render, README, .env.example  | Bonus, CE              | ALL                |

---

**¿Cómo avanzar?**
- Empezá siempre por el más arriba posible SIN dependencias activas.
- Creá el change con `/opsx:propose [change-name]` y generá/ajustá proposal, design y tasks.
- Solo cuando esté cerrado y archivado, desbloqueás los hijos dependientes.
- Si un feature o historia falta, agregalo abajo y justificá.

---