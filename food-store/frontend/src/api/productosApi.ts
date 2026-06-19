import { axiosClient } from "./axiosClient";
import type { Ingrediente, PaginatedProductos, ProductoDetail, ProductoRead } from "../types";

export interface ProductosFiltro {
  categoria?: number;
  disponible?: boolean;
  search?: string;
  page?: number;
  size?: number;
}

export interface ProductoCreateData {
  nombre: string;
  descripcion?: string | null;
  precio_base: number;
  stock_cantidad: number;
  categoria_ids: number[];
  ingrediente_ids: number[];
}

export interface ProductoUpdateData {
  nombre?: string;
  descripcion?: string | null;
  precio_base?: number;
  stock_cantidad?: number;
  disponible?: boolean;
  categoria_ids?: number[];
  ingrediente_ids?: number[];
}

export const productosApi = {
  list: (filtro: ProductosFiltro) =>
    axiosClient.get<PaginatedProductos>("/api/v1/productos", { params: filtro }).then((r) => r.data),

  get: (id: number) => axiosClient.get<ProductoDetail>(`/api/v1/productos/${id}`).then((r) => r.data),

  create: (data: ProductoCreateData) =>
    axiosClient.post<ProductoRead>("/api/v1/productos", data).then((r) => r.data),

  update: (id: number, data: ProductoUpdateData) =>
    axiosClient.put<ProductoRead>(`/api/v1/productos/${id}`, data).then((r) => r.data),

  setDisponibilidad: (id: number, disponible: boolean) =>
    axiosClient.patch<ProductoRead>(`/api/v1/productos/${id}/disponibilidad`, { disponible }).then((r) => r.data),

  setStock: (id: number, stock_cantidad: number) =>
    axiosClient.patch<ProductoRead>(`/api/v1/productos/${id}/stock`, { stock_cantidad }).then((r) => r.data),

  remove: (id: number) => axiosClient.delete(`/api/v1/productos/${id}`),
};

export const ingredientesApi = {
  list: () => axiosClient.get<Ingrediente[]>("/api/v1/ingredientes").then((r) => r.data),

  create: (data: { nombre: string; es_alergeno: boolean }) =>
    axiosClient.post<Ingrediente>("/api/v1/ingredientes", data).then((r) => r.data),

  remove: (id: number) => axiosClient.delete(`/api/v1/ingredientes/${id}`),
};
