import { useState } from "react";
import { Sandwich, Plus, SlidersHorizontal } from "lucide-react";
import type { ProductoRead } from "../../types";
import { useCartStore } from "../../store/cartStore";
import { useToast } from "../../components/Toast";
import { Button } from "../../components/Button";
import { Badge } from "../../components/Badge";
import { ProductDetailModal } from "./ProductDetailModal";

export function ProductCard({ producto }: { producto: ProductoRead }) {
  const [personalizando, setPersonalizando] = useState(false);
  const addItem = useCartStore((s) => s.addItem);
  const toast = useToast();

  const sinStock = !producto.disponible || producto.stock_cantidad === 0;

  const agregarRapido = () => {
    addItem({
      producto_id: producto.id,
      nombre: producto.nombre,
      precio_base: Number(producto.precio_base),
      cantidad: 1,
      personalizacion: [],
      ingredientesRemovidosNombres: [],
    });
    toast.show(`${producto.nombre} agregado al carrito`, "success");
  };

  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-line bg-surface p-4 transition-shadow hover:shadow-ticket">
      <div className="flex h-28 items-center justify-center rounded-xl bg-mostaza-50 text-mostaza-300">
        <Sandwich size={40} strokeWidth={1.5} />
      </div>

      <div className="flex-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-display font-semibold leading-snug">{producto.nombre}</h3>
          {sinStock && <Badge tone="danger">Sin stock</Badge>}
        </div>
        {producto.descripcion && (
          <p className="mt-1 line-clamp-2 text-sm text-ink-soft">{producto.descripcion}</p>
        )}
      </div>

      <div className="flex items-center justify-between">
        <span className="font-mono text-lg font-semibold tabular">
          ${Number(producto.precio_base).toFixed(2)}
        </span>
        <button
          onClick={() => setPersonalizando(true)}
          className="flex items-center gap-1 text-xs font-medium text-ink-soft hover:text-mostaza-600"
        >
          <SlidersHorizontal size={13} /> Personalizar
        </button>
      </div>

      <Button onClick={agregarRapido} disabled={sinStock} className="w-full">
        <Plus size={16} /> Agregar
      </Button>

      {personalizando && (
        <ProductDetailModal productoId={producto.id} onClose={() => setPersonalizando(false)} />
      )}
    </div>
  );
}
