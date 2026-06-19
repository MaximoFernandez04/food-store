import { useNavigate } from "react-router-dom";
import { ShoppingBag, X } from "lucide-react";
import { useUiStore } from "../../store/uiStore";
import { useCartStore } from "../../store/cartStore";
import { useAuthStore } from "../../store/authStore";
import { CartItemRow } from "./CartItemRow";
import { Button } from "../../components/Button";
import { EmptyState } from "../../components/EmptyState";

export function CartDrawer() {
  const cartOpen = useUiStore((s) => s.cartOpen);
  const closeCart = useUiStore((s) => s.closeCart);
  const items = useCartStore((s) => s.items);
  const subtotal = useCartStore((s) => s.subtotal());
  const costoEnvio = useCartStore((s) => s.costoEnvio());
  const total = useCartStore((s) => s.total());
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const navigate = useNavigate();

  if (!cartOpen) return null;

  const irACheckout = () => {
    closeCart();
    navigate(isAuthenticated ? "/checkout" : "/login");
  };

  return (
    <div className="fixed inset-0 z-40 flex justify-end">
      <div className="absolute inset-0 bg-ink/40" onClick={closeCart} aria-hidden="true" />
      <aside className="relative z-10 flex h-full w-full max-w-md flex-col bg-surface shadow-ticket">
        <div className="flex items-center justify-between border-b border-line px-5 py-4">
          <h2 className="font-display text-lg font-semibold">Tu carrito</h2>
          <button onClick={closeCart} aria-label="Cerrar carrito" className="rounded-full p-1.5 hover:bg-ink/5">
            <X size={18} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-5">
          {items.length === 0 ? (
            <div className="py-10">
              <EmptyState icon={<ShoppingBag size={32} />} title="Tu carrito está vacío" />
            </div>
          ) : (
            items.map((item) => (
              <CartItemRow key={`${item.producto_id}-${item.personalizacion.join(",")}`} item={item} />
            ))
          )}
        </div>

        {items.length > 0 && (
          <div className="border-t border-line px-5 py-4">
            <div className="flex justify-between text-sm text-ink-soft">
              <span>Subtotal</span>
              <span className="font-mono tabular">${subtotal.toFixed(2)}</span>
            </div>
            <div className="mt-1 flex justify-between text-sm text-ink-soft">
              <span>Envío</span>
              <span className="font-mono tabular">${costoEnvio.toFixed(2)}</span>
            </div>
            <div className="mt-2 flex justify-between font-display text-lg font-semibold">
              <span>Total</span>
              <span className="font-mono tabular">${total.toFixed(2)}</span>
            </div>
            <Button onClick={irACheckout} className="mt-4 w-full" size="lg">
              Ir a pagar
            </Button>
          </div>
        )}
      </aside>
    </div>
  );
}
