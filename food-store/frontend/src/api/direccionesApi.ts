import { axiosClient } from "./axiosClient";
import type { DireccionEntrega } from "../types";

export interface DireccionData {
  alias?: string | null;
  linea1: string;
  linea2?: string | null;
  es_principal?: boolean;
}

export const direccionesApi = {
  list: () => axiosClient.get<DireccionEntrega[]>("/api/v1/direcciones").then((r) => r.data),

  create: (data: DireccionData) =>
    axiosClient.post<DireccionEntrega>("/api/v1/direcciones", data).then((r) => r.data),

  update: (id: number, data: Partial<DireccionData>) =>
    axiosClient.put<DireccionEntrega>(`/api/v1/direcciones/${id}`, data).then((r) => r.data),

  setPrincipal: (id: number) =>
    axiosClient.patch<DireccionEntrega>(`/api/v1/direcciones/${id}/principal`).then((r) => r.data),

  remove: (id: number) => axiosClient.delete(`/api/v1/direcciones/${id}`),
};
