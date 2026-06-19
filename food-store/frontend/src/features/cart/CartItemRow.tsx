import { Minus, Plus, X } from "lucide-react";
import type { CartItem } from "../../types";
import { useCartStore } from "../../store/cartStore";

export function CartItemRow({ item }: { item: CartItem }) {
  const updateCantidad = useCartStore((s) => s.updateCantidad);
  const removeItem = useCartStore((s) => s.removeItem);

  return (
    <div className="flex gap-3 border-b border-line py-4">
      <div className="flex-1">
        <p className="font-medium">{item.nombre}</p>
        {item.ingredientesRemovidosNombres.length > 0 && (
          <p className="text-xs text-ink-soft">Sin: {item.ingredientesRemovidosNombres.join(", ")}</p>
        )}
        <p className="mt-1 font-mono text-sm tabular text-ink-soft">${item.precio_base.toFixed(2)} c/u</p>
      </div>

      <div className="flex flex-col items-end justify-between">
        <button
          onClick={() => removeItem(item.producto_id, item.personalizacion)}
          aria-label={`Quitar ${item.nombre} del carrito`}
          className="text-ink-soft hover:text-brasa-500"
        >
          <X size={16} />
        </button>
        <div className="flex items-center gap-2">
          <button
            onClick={() => updateCantidad(item.producto_id, item.personalizacion, item.cantidad - 1)}
            aria-label="Restar"
            className="rounded-full border border-line p-1 hover:bg-ink/5"
          >
            <Minus size={12} />
          </button>
          <span className="w-5 text-center font-mono text-sm tabular">{item.cantidad}</span>
          <button
            onClick={() => updateCantidad(item.producto_id, item.personalizacion, item.cantidad + 1)}
            aria-label="Sumar"
            className="rounded-full border border-line p-1 hover:bg-ink/5"
          >
            <Plus size={12} />
          </button>
        </div>
      </div>
    </div>
  );
}
