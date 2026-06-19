import { useState } from "react";
import { Plus, Trash2, Pencil, Check, X } from "lucide-react";
import { useCategorias, useCreateCategoria, useDeleteCategoria, useUpdateCategoria } from "../../hooks/useCategorias";
import { useUiStore } from "../../store/uiStore";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import { Button } from "../../components/Button";
import { Input } from "../../components/Input";
import { RowSkeleton } from "../../components/Skeleton";

export function CategoriasAdminPage() {
  const { data: categorias, isLoading } = useCategorias();
  const crear = useCreateCategoria();
  const actualizar = useUpdateCategoria();
  const eliminar = useDeleteCategoria();
  const openConfirmModal = useUiStore((s) => s.openConfirmModal);
  const toast = useToast();

  const [nuevoNombre, setNuevoNombre] = useState("");
  const [nuevoParentId, setNuevoParentId] = useState<string>("");
  const [editandoId, setEditandoId] = useState<number | null>(null);
  const [editandoNombre, setEditandoNombre] = useState("");

  const agregar = async () => {
    if (!nuevoNombre.trim()) return;
    try {
      await crear.mutateAsync({ nombre: nuevoNombre, parent_id: nuevoParentId ? Number(nuevoParentId) : null });
      setNuevoNombre("");
      setNuevoParentId("");
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  const guardarEdicion = async (id: number) => {
    try {
      await actualizar.mutateAsync({ id, data: { nombre: editandoNombre } });
      setEditandoId(null);
    } catch (err) {
      toast.show(getApiErrorMessage(err), "error");
    }
  };

  const borrar = (id: number, nombre: string) => {
    openConfirmModal({
      title: "Eliminar categoría",
      message: `¿Eliminar "${nombre}"? Si tiene productos o subcategorías activas, el backend va a rechazar el borrado.`,
      danger: true,
      onConfirm: async () => {
        try {
          await eliminar.mutateAsync(id);
          toast.show("Categoría eliminada", "success");
        } catch (err) {
          toast.show(getApiErrorMessage(err), "error");
        }
      },
    });
  };

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl font-bold">Categorías</h1>

      <div className="rounded-2xl border border-line bg-surface p-4">
        <div className="flex gap-2">
          <Input
            placeholder="Nombre de la categoría"
            value={nuevoNombre}
            onChange={(e) => setNuevoNombre(e.target.value)}
            className="flex-1"
          />
          <select
            value={nuevoParentId}
            onChange={(e) => setNuevoParentId(e.target.value)}
            className="rounded-lg border border-line bg-surface px-3 text-sm"
          >
            <option value="">Sin categoría padre</option>
            {categorias?.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nombre}
              </option>
            ))}
          </select>
          <Button onClick={agregar} loading={crear.isPending}>
            <Plus size={16} /> Agregar
          </Button>
        </div>
      </div>

      <div className="rounded-2xl border border-line bg-surface">
        {isLoading ? (
          <div className="flex flex-col gap-2 p-4">
            <RowSkeleton />
            <RowSkeleton />
          </div>
        ) : (
          <ul className="divide-y divide-line">
            {categorias?.map((cat) => (
              <li key={cat.id} className="flex items-center justify-between gap-3 p-4">
                {editandoId === cat.id ? (
                  <>
                    <Input
                      value={editandoNombre}
                      onChange={(e) => setEditandoNombre(e.target.value)}
                      className="flex-1"
                    />
                    <button onClick={() => guardarEdicion(cat.id)} className="text-oliva-500 hover:text-oliva-600">
                      <Check size={18} />
                    </button>
                    <button onClick={() => setEditandoId(null)} className="text-ink-soft hover:text-ink">
                      <X size={18} />
                    </button>
                  </>
                ) : (
                  <>
                    <span>
                      {cat.parent_id && <span className="mr-1 text-ink-soft">↳</span>}
                      {cat.nombre}
                    </span>
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          setEditandoId(cat.id);
                          setEditandoNombre(cat.nombre);
                        }}
                        className="text-ink-soft hover:text-ink"
                        aria-label={`Editar ${cat.nombre}`}
                      >
                        <Pencil size={16} />
                      </button>
                      <button
                        onClick={() => borrar(cat.id, cat.nombre)}
                        className="text-ink-soft hover:text-brasa-500"
                        aria-label={`Eliminar ${cat.nombre}`}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
