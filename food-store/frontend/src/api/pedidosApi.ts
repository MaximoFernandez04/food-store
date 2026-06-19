import { axiosClient } from "./axiosClient";
import type { CrearPedidoRequest, HistorialRead, PaginatedPedidos, PedidoDetail, PedidoRead } from "../types";

export interface PedidosFiltro {
  estado?: string;
  page?: number;
  size?: number;
}

export const pedidosApi = {
  list: (filtro: PedidosFiltro) =>
    axiosClient.get<PaginatedPedidos>("/api/v1/pedidos", { params: filtro }).then((r) => r.data),

  get: (id: number) => axiosClient.get<PedidoDetail>(`/api/v1/pedidos/${id}`).then((r) => r.data),

  create: (data: CrearPedidoRequest) =>
    axiosClient.post<PedidoRead>("/api/v1/pedidos", data).then((r) => r.data),

  avanzarEstado: (id: number, nuevo_estado: string, motivo?: string) =>
    axiosClient.patch<PedidoRead>(`/api/v1/pedidos/${id}/estado`, { nuevo_estado, motivo }).then((r) => r.data),

  historial: (id: number) =>
    axiosClient.get<HistorialRead[]>(`/api/v1/pedidos/${id}/historial`).then((r) => r.data),
};
