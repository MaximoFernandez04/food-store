import { useState } from "react";
import { UtensilsCrossed, ChevronLeft, ChevronRight } from "lucide-react";
import { useProductos } from "../../hooks/useProductos";
import { useDebounce } from "../../hooks/useDebounce";
import { ProductCard } from "./ProductCard";
import { ProductFilters } from "./ProductFilters";
import { ProductCardSkeleton } from "../../components/Skeleton";
import { EmptyState } from "../../components/EmptyState";
import { Button } from "../../components/Button";

const PAGE_SIZE = 12;

export function CatalogoGrid() {
  const [search, setSearch] = useState("");
  const [categoriaId, setCategoriaId] = useState<number | undefined>(undefined);
  const [page, setPage] = useState(1);
  const searchDebounced = useDebounce(search, 350);

  const { data, isLoading, isFetching } = useProductos({
    search: searchDebounced || undefined,
    categoria: categoriaId,
    disponible: true,
    page,
    size: PAGE_SIZE,
  });

  const totalPaginas = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-6">
        <h1 className="font-display text-3xl font-bold">El menú de hoy</h1>
        <p className="mt-1 text-ink-soft">Elegí, personalizá y pagá online.</p>
      </div>

      <div className="mb-6">
        <ProductFilters
          search={search}
          onSearchChange={(v) => {
            setSearch(v);
            setPage(1);
          }}
          categoriaId={categoriaId}
          onCategoriaChange={(id) => {
            setCategoriaId(id);
            setPage(1);
          }}
        />
      </div>

      {isLoading ? (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <ProductCardSkeleton key={i} />
          ))}
        </div>
      ) : data && data.items.length > 0 ? (
        <>
          <div
            className={`grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 transition-opacity ${
              isFetching ? "opacity-60" : ""
            }`}
          >
            {data.items.map((producto) => (
              <ProductCard key={producto.id} producto={producto} />
            ))}
          </div>

          {totalPaginas > 1 && (
            <div className="mt-8 flex items-center justify-center gap-3">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                <ChevronLeft size={16} />
              </Button>
              <span className="text-sm text-ink-soft">
                Página {page} de {totalPaginas}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setPage((p) => Math.min(totalPaginas, p + 1))}
                disabled={page === totalPaginas}
              >
                <ChevronRight size={16} />
              </Button>
            </div>
          )}
        </>
      ) : (
        <EmptyState
          icon={<UtensilsCrossed size={36} />}
          title="No encontramos productos"
          description="Probá con otra búsqueda o mirá otra categoría."
        />
      )}
    </div>
  );
}
