import { useState } from "react";
import { Minus, Plus } from "lucide-react";
import { Modal } from "../../components/Modal";
import { Button } from "../../components/Button";
import { Skeleton } from "../../components/Skeleton";
import { Badge } from "../../components/Badge";
import { useProducto } from "../../hooks/useProductos";
import { useCartStore } from "../../store/cartStore";
import { useToast } from "../../components/Toast";

export function ProductDetailModal({ productoId, onClose }: { productoId: number; onClose: () => void }) {
  const { data: producto, isLoading } = useProducto(productoId);
  const [cantidad, setCantidad] = useState(1);
  const [removidos, setRemovidos] = useState<number[]>([]);
  const addItem = useCartStore((s) => s.addItem);
  const toast = useToast();

  const toggleIngrediente = (id: number) =>
    setRemovidos((prev) => (prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]));

  const confirmar = () => {
    if (!producto) return;
    const removibles = producto.ingredientes.filter((i) => i.es_removible);
    const nombresRemovidos = removibles.filter((i) => removidos.includes(i.id)).map((i) => i.nombre);
    addItem({
      producto_id: producto.id,
      nombre: producto.nombre,
      precio_base: Number(producto.precio_base),
      cantidad,
      personalizacion: removidos,
      ingredientesRemovidosNombres: nombresRemovidos,
    });
    toast.show(`${producto.nombre} agregado al carrito`, "success");
    onClose();
  };

  const removibles = producto?.ingredientes.filter((i) => i.es_removible) ?? [];

  return (
    <Modal open onClose={onClose} title={producto?.nombre ?? "Producto"}>
      {isLoading || !producto ? (
        <div className="flex flex-col gap-3">
          <Skeleton className="h-4 w-2/3" />
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-10 w-full" />
        </div>
      ) : (
        <div className="flex flex-col gap-5">
          {producto.descripcion && <p className="text-sm text-ink-soft">{producto.descripcion}</p>}

          {removibles.length > 0 && (
            <div>
              <h4 className="mb-2 text-sm font-semibold">Sacar ingredientes</h4>
              <div className="flex flex-col gap-2">
                {removibles.map((ing) => (
                  <label key={ing.id} className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={removidos.includes(ing.id)}
                      onChange={() => toggleIngrediente(ing.id)}
                      className="h-4 w-4 rounded border-line text-mostaza-500 focus:ring-mostaza-500"
                    />
                    {ing.nombre}
                    {ing.es_alergeno && <Badge tone="warning">Alérgeno</Badge>}
                  </label>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-ink-soft">Cantidad</span>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setCantidad((c) => Math.max(1, c - 1))}
                aria-label="Restar cantidad"
                className="rounded-full border border-line p-1.5 hover:bg-ink/5"
              >
                <Minus size={14} />
              </button>
              <span className="w-6 text-center font-mono tabular">{cantidad}</span>
              <button
                onClick={() => setCantidad((c) => Math.min(producto.stock_cantidad, c + 1))}
                aria-label="Sumar cantidad"
                className="rounded-full border border-line p-1.5 hover:bg-ink/5"
              >
                <Plus size={14} />
              </button>
            </div>
          </div>

          <Button onClick={confirmar} disabled={!producto.disponible || producto.stock_cantidad === 0}>
            Agregar ${(Number(producto.precio_base) * cantidad).toFixed(2)}
          </Button>
        </div>
      )}
    </Modal>
  );
}
