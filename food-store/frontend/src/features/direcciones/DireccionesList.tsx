import { useState } from "react";
import { Plus, Store } from "lucide-react";
import { useDirecciones } from "../../hooks/useDirecciones";
import { DireccionForm } from "./DireccionForm";
import { RowSkeleton } from "../../components/Skeleton";

interface DireccionesListProps {
  selectedId: number | null;
  onSelect: (id: number | null) => void;
}

export function DireccionesList({ selectedId, onSelect }: DireccionesListProps) {
  const { data: direcciones, isLoading } = useDirecciones();
  const [agregando, setAgregando] = useState(false);

  if (isLoading) {
    return (
      <div className="flex flex-col gap-2">
        <RowSkeleton />
        <RowSkeleton />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      <label className="flex cursor-pointer items-center gap-3 rounded-xl border border-line p-3 hover:border-mostaza-300">
        <input
          type="radio"
          name="direccion"
          checked={selectedId === null}
          onChange={() => onSelect(null)}
          className="text-mostaza-500 focus:ring-mostaza-500"
        />
        <Store size={18} className="text-ink-soft" />
        <span className="text-sm font-medium">Retiro en el local</span>
      </label>

      {direcciones?.map((dir) => (
        <label
          key={dir.id}
          className="flex cursor-pointer items-start gap-3 rounded-xl border border-line p-3 hover:border-mostaza-300"
        >
          <input
            type="radio"
            name="direccion"
            checked={selectedId === dir.id}
            onChange={() => onSelect(dir.id)}
            className="mt-1 text-mostaza-500 focus:ring-mostaza-500"
          />
          <div className="text-sm">
            <p className="font-medium">{dir.alias || "Dirección"}</p>
            <p className="text-ink-soft">
              {dir.linea1}
              {dir.linea2 ? `, ${dir.linea2}` : ""}
            </p>
          </div>
        </label>
      ))}

      {agregando ? (
        <div className="rounded-xl border border-line p-3">
          <DireccionForm onCreated={() => setAgregando(false)} />
        </div>
      ) : (
        <button
          onClick={() => setAgregando(true)}
          className="flex items-center gap-2 rounded-xl border border-dashed border-line p-3 text-sm font-medium text-ink-soft hover:border-mostaza-300 hover:text-mostaza-600"
        >
          <Plus size={16} /> Agregar nueva dirección
        </button>
      )}
    </div>
  );
}
