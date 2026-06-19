import { useState } from "react";
import { usePedidos, useAvanzarEstado } from "../../hooks/usePedidos";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import { EstadoPedidoBadge } from "../../components/Badge";
import { Button } from "../../components/Button";
import { RowSkeleton } from "../../components/Skeleton";
import type { EstadoPedidoCodigo, PedidoRead } from "../../types";

const FILTROS: { value: EstadoPedidoCodigo | ""; label: string }[] = [
  { value: "", label: "Todos" },
  { value: "PENDIENTE", label: "Pendiente" },
  { value: "CONFIRMADO", label: "Confirmado" },
  { value: "EN_PREPARACION", label: "En preparación" },
  { value: "EN_CAMINO", label: "En camino" },
  { value: "ENTREGADO", label: "Entregado" },
  { value: "CANCELADO", label: "Cancelado" },
];

// Próximo estado "natural" en la FSM (sección 3.4) — el botón de avance
// muestra solo este, nunca un salto inválido.
const SIGUIENTE: Partial<Record<EstadoPedidoCodigo, { estado: EstadoPedidoCodigo; label: string }>> = {
  PENDIENTE: { estado: "CONFIRMADO", label: "Confirmar pago" },
  CONFIRMADO: { estado: "EN_PREPARACION", label: "Empezar preparación" },
  EN_PREPARACION: { estado: "EN_CAMINO", label: "Despachar" },
  EN_CAMINO: { estado: "ENTREGADO", label: "Marcar entregado" },
};

const PUEDE_CANCELAR: EstadoPedidoCodigo[] = ["PENDIENTE", "CONFIRMADO", "EN_PREPARACION"];

export function PedidosAdminPage() {
  const [estadoFiltro, setEstadoFiltro] = useState<EstadoPedidoCodigo | "">("");
  const [page, setPage] = useState(1);
  const { data, isLoading } = usePedidos({ estado: estadoFiltro || undefined, page, size: 15 });
  const avanzarEstado = useAvanzarEstado();
  const toast = useToast();

  const avanzar = async (pedido: PedidoRead, nuevoEstado: EstadoPedidoCodigo) => {
    try {
      await avanzarEstado.mutateAsync({ id: pedido.id, nuevo_estado: nuevoEstado });
      toast.show(`Pedido #${pedido.id} actualizado`, "success");
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  const cancelar = async (pedido: PedidoRead) => {
    const motivo = window.prompt("Motivo de la cancelación:");
    if (!motivo) return;
    try {
      await avanzarEstado.mutateAsync({ id: pedido.id, nuevo_estado: "CANCELADO", motivo });
      toast.show(`Pedido #${pedido.id} cancelado`, "success");
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl font-bold">Pedidos</h1>

      <div className="flex gap-2 overflow-x-auto">
        {FILTROS.map((f) => (
          <button
            key={f.value}
            onClick={() => {
              setEstadoFiltro(f.value);
              setPage(1);
            }}
            className={`whitespace-nowrap rounded-full px-3.5 py-1.5 text-sm font-medium ${
              estadoFiltro === f.value ? "bg-ink text-paper" : "bg-ink/5 text-ink-soft hover:bg-ink/10"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="overflow-x-auto rounded-2xl border border-line bg-surface">
        {isLoading ? (
          <div className="flex flex-col gap-2 p-4">
            <RowSkeleton />
            <RowSkeleton />
          </div>
        ) : data?.items.length === 0 ? (
          <p className="p-6 text-center text-sm text-ink-soft">No hay pedidos en este estado.</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-line text-left text-ink-soft">
                <th className="p-3 font-medium">Pedido</th>
                <th className="p-3 font-medium">Fecha</th>
                <th className="p-3 font-medium">Total</th>
                <th className="p-3 font-medium">Estado</th>
                <th className="p-3 font-medium text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {data?.items.map((pedido) => {
                const siguiente = SIGUIENTE[pedido.estado_codigo];
                return (
                  <tr key={pedido.id} className="border-b border-line last:border-0">
                    <td className="p-3 font-medium">#{pedido.id}</td>
                    <td className="p-3 text-ink-soft">{new Date(pedido.created_at).toLocaleDateString("es-AR")}</td>
                    <td className="p-3 font-mono tabular">${Number(pedido.total).toFixed(2)}</td>
                    <td className="p-3">
                      <EstadoPedidoBadge estado={pedido.estado_codigo} />
                    </td>
                    <td className="p-3 text-right">
                      <div className="flex justify-end gap-2">
                        {siguiente && (
                          <Button size="sm" variant="secondary" onClick={() => avanzar(pedido, siguiente.estado)}>
                            {siguiente.label}
                          </Button>
                        )}
                        {PUEDE_CANCELAR.includes(pedido.estado_codigo) && (
                          <Button size="sm" variant="danger" onClick={() => cancelar(pedido)}>
                            Cancelar
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {data && data.total > 15 && (
        <div className="flex items-center justify-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}>
            Anterior
          </Button>
          <span className="text-sm text-ink-soft">Página {page}</span>
          <Button variant="ghost" size="sm" onClick={() => setPage((p) => p + 1)} disabled={data.items.length < 15}>
            Siguiente
          </Button>
        </div>
      )}
    </div>
  );
}
