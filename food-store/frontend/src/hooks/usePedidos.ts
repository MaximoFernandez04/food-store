import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { pedidosApi, type PedidosFiltro } from "../api/pedidosApi";
import type { CrearPedidoRequest, EstadoPedidoCodigo } from "../types";

const ESTADOS_TERMINALES: EstadoPedidoCodigo[] = ["ENTREGADO", "CANCELADO"];

export function usePedidos(filtro: PedidosFiltro) {
  return useQuery({
    queryKey: ["pedidos", filtro],
    queryFn: () => pedidosApi.list(filtro),
    placeholderData: (prev) => prev,
  });
}

/** Polling cada 30s (sección 11: "Webhook / IPN... evita polling constante",
 * pero el cliente igual necesita refrescar su PANTALLA de seguimiento para
 * ver cuando el webhook confirma el pago o el staff avanza el pedido). Se
 * detiene solo al llegar a un estado terminal. */
export function usePedido(id: number) {
  return useQuery({
    queryKey: ["pedidos", id],
    queryFn: () => pedidosApi.get(id),
    refetchInterval: (query) => {
      const estado = query.state.data?.estado_codigo;
      if (estado && ESTADOS_TERMINALES.includes(estado)) return false;
      return 30_000;
    },
  });
}

export function useCrearPedido() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CrearPedidoRequest) => pedidosApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["pedidos"] }),
  });
}

export function useAvanzarEstado() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, nuevo_estado, motivo }: { id: number; nuevo_estado: string; motivo?: string }) =>
      pedidosApi.avanzarEstado(id, nuevo_estado, motivo),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ["pedidos"] });
      qc.invalidateQueries({ queryKey: ["pedidos", id] });
    },
  });
}
