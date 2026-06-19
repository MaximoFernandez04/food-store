// Tipos compartidos de dominio. Reflejan los schemas Pydantic del backend
// (sección 6 de la spec). strict: true en tsconfig — nada de `any` acá.

export type RolCodigo = "ADMIN" | "STOCK" | "PEDIDOS" | "CLIENT";

export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  roles: RolCodigo[];
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// ---------- Catálogo ----------

export interface Categoria {
  id: number;
  nombre: string;
  parent_id: number | null;
}

export interface Ingrediente {
  id: number;
  nombre: string;
  es_alergeno: boolean;
}

export interface ProductoIngrediente extends Ingrediente {
  es_removible: boolean;
}

export interface ProductoRead {
  id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  stock_cantidad: number;
  disponible: boolean;
  created_at: string;
}

export interface ProductoDetail extends ProductoRead {
  ingredientes: ProductoIngrediente[];
  categorias: Categoria[];
}

export interface PaginatedProductos {
  items: ProductoRead[];
  total: number;
  page: number;
  size: number;
}

// ---------- Direcciones ----------

export interface DireccionEntrega {
  id: number;
  alias: string | null;
  linea1: string;
  linea2: string | null;
  es_principal: boolean;
}

// ---------- Carrito (cliente, no viene del backend) ----------

export interface CartItem {
  producto_id: number;
  nombre: string;
  precio_base: number;
  cantidad: number;
  personalizacion: number[]; // IDs de ingredientes removidos
  ingredientesRemovidosNombres: string[]; // para mostrar en el carrito sin re-fetchear
}

// ---------- Pedidos ----------

export type EstadoPedidoCodigo =
  | "PENDIENTE"
  | "CONFIRMADO"
  | "EN_PREPARACION"
  | "EN_CAMINO"
  | "ENTREGADO"
  | "CANCELADO";

export interface DetallePedidoRead {
  id: number;
  producto_id: number;
  nombre_snapshot: string;
  precio_snapshot: number;
  cantidad: number;
  subtotal: number;
  personalizacion: number[] | null;
}

export interface HistorialRead {
  id: number;
  estado_desde: EstadoPedidoCodigo | null;
  estado_hasta: EstadoPedidoCodigo;
  usuario_id: number | null;
  motivo: string | null;
  created_at: string;
}

export interface PedidoRead {
  id: number;
  estado_codigo: EstadoPedidoCodigo;
  subtotal: number;
  costo_envio: number;
  total: number;
  created_at: string;
}

export interface PedidoDetail extends PedidoRead {
  forma_pago_codigo: string;
  direccion_id: number | null;
  notas: string | null;
  items: DetallePedidoRead[];
  historial: HistorialRead[];
}

export interface PaginatedPedidos {
  items: PedidoRead[];
  total: number;
  page: number;
  size: number;
}

export interface CrearPedidoRequest {
  items: {
    producto_id: number;
    cantidad: number;
    personalizacion: number[] | null;
  }[];
  forma_pago_codigo: string;
  direccion_id: number | null;
  notas: string | null;
}

// ---------- Pagos ----------

export type MpEstadoPago = "approved" | "pending" | "rejected" | "in_process" | "cancelled";

export interface PagoResponse {
  id: number;
  pedido_id: number;
  mp_payment_id: number | null;
  mp_status: MpEstadoPago;
  mp_status_detail: string | null;
  external_reference: string;
  created_at: string;
}

// ---------- Admin / Dashboard ----------

export interface ProductoMasVendido {
  producto_id: number;
  nombre: string;
  cantidad_vendida: number;
}

export interface DashboardStats {
  total_ventas: number;
  pedidos_por_estado: Record<EstadoPedidoCodigo, number>;
  productos_mas_vendidos: ProductoMasVendido[];
  total_usuarios: number;
  total_productos: number;
}

// ---------- Errores (RFC 7807 simplificado, ver sección 5 de la spec) ----------

export interface ApiErrorBody {
  detail: string;
  code: string;
  field?: string | null;
}
