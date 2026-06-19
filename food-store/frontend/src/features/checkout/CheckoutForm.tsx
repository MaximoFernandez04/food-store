import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CreditCard, Wallet, Landmark } from "lucide-react";
import { useCartStore } from "../../store/cartStore";
import { useAuthStore } from "../../store/authStore";
import { useCrearPedido } from "../../hooks/usePedidos";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import { Button } from "../../components/Button";
import { DireccionesList } from "../direcciones/DireccionesList";
import { CardPaymentForm } from "./CardPaymentForm";
import type { PagoResponse } from "../../types";

type FormaPago = "MERCADOPAGO" | "EFECTIVO" | "TRANSFERENCIA";

const FORMAS_PAGO: { codigo: FormaPago; label: string; icon: typeof CreditCard }[] = [
  { codigo: "MERCADOPAGO", label: "Tarjeta (MercadoPago)", icon: CreditCard },
  { codigo: "EFECTIVO", label: "Efectivo al recibir", icon: Wallet },
  { codigo: "TRANSFERENCIA", label: "Transferencia bancaria", icon: Landmark },
];

export function CheckoutForm() {
  const items = useCartStore((s) => s.items);
  const subtotal = useCartStore((s) => s.subtotal());
  const costoEnvio = useCartStore((s) => s.costoEnvio());
  const total = useCartStore((s) => s.total());
  const clearCart = useCartStore((s) => s.clearCart);
  const usuario = useAuthStore((s) => s.usuario);

  const [direccionId, setDireccionId] = useState<number | null>(null);
  const [formaPago, setFormaPago] = useState<FormaPago>("MERCADOPAGO");
  const [pedidoCreado, setPedidoCreado] = useState<{ id: number } | null>(null);

  const crearPedido = useCrearPedido();
  const toast = useToast();
  const navigate = useNavigate();

  const confirmarPedido = async () => {
    try {
      const pedido = await crearPedido.mutateAsync({
        items: items.map((i) => ({
          producto_id: i.producto_id,
          cantidad: i.cantidad,
          personalizacion: i.personalizacion.length > 0 ? i.personalizacion : null,
        })),
        forma_pago_codigo: formaPago,
        direccion_id: direccionId,
        notas: null,
      });
      setPedidoCreado(pedido);
      if (formaPago !== "MERCADOPAGO") {
        clearCart();
        toast.show("Pedido creado. Te vamos a confirmar el pago manualmente.", "success");
        navigate(`/pedidos/${pedido.id}`);
      }
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  const onResultadoPago = (pago: PagoResponse) => {
    if (!pedidoCreado) return;
    clearCart();
    if (pago.mp_status === "approved") {
      toast.show("¡Pago aprobado! Tu pedido fue confirmado.", "success");
    } else if (pago.mp_status === "rejected") {
      toast.show("El pago fue rechazado. Podés reintentar desde tu pedido.", "error");
    } else {
      toast.show("Pago en proceso. Te avisamos cuando se confirme.", "info");
    }
    navigate(`/pedidos/${pedidoCreado.id}`);
  };

  if (items.length === 0 && !pedidoCreado) {
    return <p className="text-center text-ink-soft">Tu carrito está vacío.</p>;
  }

  // Paso 2: ya se creó el pedido y eligió MercadoPago -> mostrar el Brick.
  if (pedidoCreado && formaPago === "MERCADOPAGO") {
    return (
      <div className="rounded-2xl border border-line bg-surface p-6 shadow-ticket">
        <h2 className="mb-4 font-display text-lg font-semibold">Pagá con tarjeta</h2>
        <CardPaymentForm
          pedidoId={pedidoCreado.id}
          amount={total}
          payerEmail={usuario?.email ?? ""}
          onResultado={onResultadoPago}
        />
      </div>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="flex flex-col gap-6">
        <section>
          <h2 className="mb-3 font-display text-lg font-semibold">¿Dónde lo recibís?</h2>
          <DireccionesList selectedId={direccionId} onSelect={setDireccionId} />
        </section>

        <section>
          <h2 className="mb-3 font-display text-lg font-semibold">¿Cómo pagás?</h2>
          <div className="flex flex-col gap-2">
            {FORMAS_PAGO.map(({ codigo, label, icon: Icon }) => (
              <label
                key={codigo}
                className="flex cursor-pointer items-center gap-3 rounded-xl border border-line p-3 hover:border-mostaza-300"
              >
                <input
                  type="radio"
                  name="formaPago"
                  checked={formaPago === codigo}
                  onChange={() => setFormaPago(codigo)}
                  className="text-mostaza-500 focus:ring-mostaza-500"
                />
                <Icon size={18} className="text-ink-soft" />
                <span className="text-sm font-medium">{label}</span>
              </label>
            ))}
          </div>
        </section>
      </div>

      <aside className="h-fit rounded-2xl border border-line bg-surface p-5 shadow-ticket">
        <h2 className="mb-3 font-display text-lg font-semibold">Resumen</h2>
        <ul className="mb-4 flex flex-col gap-2 text-sm">
          {items.map((item) => (
            <li key={`${item.producto_id}-${item.personalizacion.join(",")}`} className="flex justify-between">
              <span className="text-ink-soft">
                {item.cantidad}× {item.nombre}
              </span>
              <span className="font-mono tabular">${(item.precio_base * item.cantidad).toFixed(2)}</span>
            </li>
          ))}
        </ul>
        <div className="flex justify-between border-t border-line pt-3 text-sm text-ink-soft">
          <span>Subtotal</span>
          <span className="font-mono tabular">${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm text-ink-soft">
          <span>Envío</span>
          <span className="font-mono tabular">${costoEnvio.toFixed(2)}</span>
        </div>
        <div className="mt-2 flex justify-between font-display text-lg font-semibold">
          <span>Total</span>
          <span className="font-mono tabular">${total.toFixed(2)}</span>
        </div>

        <Button onClick={confirmarPedido} loading={crearPedido.isPending} className="mt-5 w-full" size="lg">
          Confirmar pedido
        </Button>
      </aside>
    </div>
  );
}
