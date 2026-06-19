import { axiosClient } from "./axiosClient";
import type { PagoResponse } from "../types";

export interface CrearPagoData {
  pedido_id: number;
  token: string;
  payer_email: string;
  installments?: number;
}

export const pagosApi = {
  crear: (data: CrearPagoData) =>
    axiosClient.post<PagoResponse>("/api/v1/pagos/crear", data).then((r) => r.data),

  getDePedido: (pedidoId: number) =>
    axiosClient.get<PagoResponse>(`/api/v1/pagos/${pedidoId}`).then((r) => r.data),
};
