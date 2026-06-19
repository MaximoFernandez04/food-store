import { Search } from "lucide-react";
import { useCategorias } from "../../hooks/useCategorias";

interface ProductFiltersProps {
  search: string;
  onSearchChange: (value: string) => void;
  categoriaId: number | undefined;
  onCategoriaChange: (id: number | undefined) => void;
}

export function ProductFilters({ search, onSearchChange, categoriaId, onCategoriaChange }: ProductFiltersProps) {
  const { data: categorias } = useCategorias();

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <div className="relative flex-1">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft" />
        <input
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Buscar en el menú…"
          className="w-full rounded-lg border border-line bg-surface py-2.5 pl-9 pr-3 text-sm focus:border-mostaza-500 focus:outline-none"
        />
      </div>

      <div className="flex gap-2 overflow-x-auto">
        <button
          onClick={() => onCategoriaChange(undefined)}
          className={`whitespace-nowrap rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors ${
            categoriaId === undefined ? "bg-ink text-paper" : "bg-ink/5 text-ink-soft hover:bg-ink/10"
          }`}
        >
          Todo
        </button>
        {categorias?.map((cat) => (
          <button
            key={cat.id}
            onClick={() => onCategoriaChange(cat.id)}
            className={`whitespace-nowrap rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors ${
              categoriaId === cat.id ? "bg-ink text-paper" : "bg-ink/5 text-ink-soft hover:bg-ink/10"
            }`}
          >
            {cat.nombre}
          </button>
        ))}
      </div>
    </div>
  );
}
