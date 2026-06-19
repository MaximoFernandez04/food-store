import { useMutation, useQueryClient } from "@tanstack/react-query";
import { pagosApi, type CrearPagoData } from "../api/pagosApi";

export function useCrearPago() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: CrearPagoData) => pagosApi.crear(data),
    onSuccess: (_, { pedido_id }) => {
      qc.invalidateQueries({ queryKey: ["pedidos", pedido_id] });
      qc.invalidateQueries({ queryKey: ["pedidos"] });
    },
  });
}
