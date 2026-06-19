import { axiosClient } from "./axiosClient";
import type { Categoria } from "../types";

export const categoriasApi = {
  list: () => axiosClient.get<Categoria[]>("/api/v1/categorias").then((r) => r.data),

  create: (data: { nombre: string; parent_id?: number | null }) =>
    axiosClient.post<Categoria>("/api/v1/categorias", data).then((r) => r.data),

  update: (id: number, data: { nombre: string; parent_id?: number | null }) =>
    axiosClient.put<Categoria>(`/api/v1/categorias/${id}`, data).then((r) => r.data),

  remove: (id: number) => axiosClient.delete(`/api/v1/categorias/${id}`),
};
