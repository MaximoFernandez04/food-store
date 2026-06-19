import { useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";
import {
  useProductos,
  useDeleteProducto,
  useSetDisponibilidad,
  useSetStock,
} from "../../hooks/useProductos";
import { useUiStore } from "../../store/uiStore";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import { Button } from "../../components/Button";
import { RowSkeleton } from "../../components/Skeleton";
import { ProductoFormModal } from "./ProductoFormModal";

const PAGE_SIZE = 10;

export function ProductosAdminPage() {
  const [page, setPage] = useState(1);
  const [modalProductoId, setModalProductoId] = useState<number | null | "nuevo">(null);
  const { data, isLoading } = useProductos({ page, size: PAGE_SIZE });
  const setDisponibilidad = useSetDisponibilidad();
  const setStock = useSetStock();
  const eliminar = useDeleteProducto();
  const openConfirmModal = useUiStore((s) => s.openConfirmModal);
  const toast = useToast();

  const [stockEditando, setStockEditando] = useState<Record<number, string>>({});

  const guardarStock = async (id: number) => {
    const valor = Number(stockEditando[id]);
    if (Number.isNaN(valor) || valor < 0) return;
    try {
      await setStock.mutateAsync({ id, stock_cantidad: valor });
      toast.show("Stock actualizado", "success");
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  const borrar = (id: number, nombre: string) => {
    openConfirmModal({
      title: "Eliminar producto",
      message: `¿Eliminar "${nombre}" del catálogo?`,
      danger: true,
      onConfirm: async () => {
        try {
          await eliminar.mutateAsync(id);
          toast.show("Producto eliminado", "success");
        } catch (err) {
          toast.show(getApiErrorMessage(err), "error");
        }
      },
    });
  };

  const totalPaginas = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl font-bold">Productos</h1>
        <Button onClick={() => setModalProductoId("nuevo")}>
          <Plus size={16} /> Nuevo producto
        </Button>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-line bg-surface">
        {isLoading ? (
          <div className="flex flex-col gap-2 p-4">
            <RowSkeleton />
            <RowSkeleton />
            <RowSkeleton />
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-line text-left text-ink-soft">
                <th className="p-3 font-medium">Producto</th>
                <th className="p-3 font-medium">Precio</th>
                <th className="p-3 font-medium">Stock</th>
                <th className="p-3 font-medium">Disponible</th>
                <th className="p-3 font-medium text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {data?.items.map((producto) => (
                <tr key={producto.id} className="border-b border-line last:border-0">
                  <td className="p-3 font-medium">{producto.nombre}</td>
                  <td className="p-3 font-mono tabular">${Number(producto.precio_base).toFixed(2)}</td>
                  <td className="p-3">
                    <input
                      type="number"
                      defaultValue={producto.stock_cantidad}
                      onChange={(e) => setStockEditando((s) => ({ ...s, [producto.id]: e.target.value }))}
                      onBlur={() => guardarStock(producto.id)}
                      className="w-20 rounded-lg border border-line px-2 py-1 font-mono tabular"
                    />
                  </td>
                  <td className="p-3">
                    <button
                      role="switch"
                      aria-checked={producto.disponible}
                      onClick={() =>
                        setDisponibilidad.mutate({ id: producto.id, disponible: !producto.disponible })
                      }
                      className={`h-5 w-9 rounded-full transition-colors ${
                        producto.disponible ? "bg-oliva-500" : "bg-ink/15"
                      }`}
                    >
                      <span
                        className={`block h-4 w-4 translate-x-0.5 rounded-full bg-white transition-transform ${
                          producto.disponible ? "translate-x-[18px]" : ""
                        }`}
                      />
                    </button>
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => setModalProductoId(producto.id)}
                      className="mr-2 text-ink-soft hover:text-ink"
                      aria-label={`Editar ${producto.nombre}`}
                    >
                      <Pencil size={16} />
                    </button>
                    <button
                      onClick={() => borrar(producto.id, producto.nombre)}
                      className="text-ink-soft hover:text-brasa-500"
                      aria-label={`Eliminar ${producto.nombre}`}
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {totalPaginas > 1 && (
        <div className="flex items-center justify-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}>
            Anterior
          </Button>
          <span className="text-sm text-ink-soft">
            {page} / {totalPaginas}
          </span>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setPage((p) => Math.min(totalPaginas, p + 1))}
            disabled={page === totalPaginas}
          >
            Siguiente
          </Button>
        </div>
      )}

      {modalProductoId !== null && (
        <ProductoFormModal
          productoId={modalProductoId === "nuevo" ? null : modalProductoId}
          onClose={() => setModalProductoId(null)}
        />
      )}
    </div>
  );
}
