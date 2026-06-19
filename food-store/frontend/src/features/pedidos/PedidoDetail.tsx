import { useState } from "react";
import { useParams } from "react-router-dom";
import { usePedido, useAvanzarEstado } from "../../hooks/usePedidos";
import { useAuthStore } from "../../store/authStore";
import { useUiStore } from "../../store/uiStore";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import { EstadoPedidoBadge } from "../../components/Badge";
import { Button } from "../../components/Button";
import { Skeleton } from "../../components/Skeleton";
import { HistorialTimeline } from "./HistorialTimeline";
import { CardPaymentForm } from "../checkout/CardPaymentForm";

export function PedidoDetail() {
  const { id } = useParams();
  const pedidoId = Number(id);
  const { data: pedido, isLoading } = usePedido(pedidoId);
  const usuario = useAuthStore((s) => s.usuario);
  const openConfirmModal = useUiStore((s) => s.openConfirmModal);
  const avanzarEstado = useAvanzarEstado();
  const toast = useToast();
  const [reintentandoPago, setReintentandoPago] = useState(false);

  if (isLoading || !pedido) {
    return (
      <div className="flex flex-col gap-3">
        <Skeleton className="h-8 w-40" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  const puedeCancelar = ["PENDIENTE", "CONFIRMADO"].includes(pedido.estado_codigo);
  const puedeReintentar = pedido.estado_codigo === "PENDIENTE" && pedido.forma_pago_codigo === "MERCADOPAGO";

  const cancelar = () => {
    openConfirmModal({
      title: "Cancelar pedido",
      message: "¿Seguro que querés cancelar este pedido? Esta acción no se puede deshacer.",
      confirmLabel: "Sí, cancelar",
      danger: true,
      onConfirm: async () => {
        try {
          await avanzarEstado.mutateAsync({ id: pedido.id, nuevo_estado: "CANCELADO", motivo: "Cancelado por el cliente" });
          toast.show("Pedido cancelado", "success");
        } catch (err) {
          toast.show(getApiErrorMessage(err), "error");
        }
      },
    });
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="flex flex-col gap-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display text-2xl font-bold">Pedido #{pedido.id}</h1>
            <EstadoPedidoBadge estado={pedido.estado_codigo} />
          </div>
          <p className="text-sm text-ink-soft">{new Date(pedido.created_at).toLocaleString("es-AR")}</p>
        </div>

        <div className="rounded-2xl border border-line bg-surface p-5">
          <h2 className="mb-3 font-display font-semibold">Tu pedido</h2>
          <ul className="flex flex-col gap-2 text-sm">
            {pedido.items.map((item) => (
              <li key={item.id} className="flex justify-between">
                <span>
                  {item.cantidad}× {item.nombre_snapshot}
                </span>
                <span className="font-mono tabular">${Number(item.subtotal).toFixed(2)}</span>
              </li>
            ))}
          </ul>
          <div className="mt-3 flex justify-between border-t border-line pt-3 font-semibold">
            <span>Total</span>
            <span className="font-mono tabular">${Number(pedido.total).toFixed(2)}</span>
          </div>
        </div>

        <HistorialTimeline historial={pedido.historial} />

        {puedeReintentar && (
          <div className="rounded-2xl border border-line bg-surface p-5">
            {reintentandoPago ? (
              <CardPaymentForm
                pedidoId={pedido.id}
                amount={Number(pedido.total)}
                payerEmail={usuario?.email ?? ""}
                onResultado={() => setReintentandoPago(false)}
              />
            ) : (
              <Button onClick={() => setReintentandoPago(true)} className="w-full">
                Pagar ahora
              </Button>
            )}
          </div>
        )}
      </div>

      <aside className="h-fit rounded-2xl border border-line bg-surface p-5">
        {puedeCancelar && (
          <Button variant="danger" onClick={cancelar} className="w-full" loading={avanzarEstado.isPending}>
            Cancelar pedido
          </Button>
        )}
      </aside>
    </div>
  );
}
