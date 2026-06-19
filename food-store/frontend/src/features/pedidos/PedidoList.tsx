import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ClipboardList } from "lucide-react";
import { usePedidos } from "../../hooks/usePedidos";
import { EstadoPedidoBadge } from "../../components/Badge";
import { RowSkeleton } from "../../components/Skeleton";
import { EmptyState } from "../../components/EmptyState";
import { Button } from "../../components/Button";

export function PedidoList() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = usePedidos({ page, size: 10 });
  const navigate = useNavigate();

  if (isLoading) {
    return (
      <div className="flex flex-col gap-3">
        <RowSkeleton />
        <RowSkeleton />
        <RowSkeleton />
      </div>
    );
  }

  if (!data || data.items.length === 0) {
    return (
      <EmptyState
        icon={<ClipboardList size={36} />}
        title="Todavía no hiciste ningún pedido"
        description="Cuando pidas algo del menú, lo vas a poder seguir acá."
        action={<Button onClick={() => navigate("/")}>Ver el menú</Button>}
      />
    );
  }

  const totalPaginas = Math.max(1, Math.ceil(data.total / 10));

  return (
    <div className="flex flex-col gap-3">
      {data.items.map((pedido) => (
        <button
          key={pedido.id}
          onClick={() => navigate(`/pedidos/${pedido.id}`)}
          className="flex items-center justify-between rounded-xl border border-line bg-surface p-4 text-left hover:border-mostaza-300"
        >
          <div>
            <p className="font-medium">Pedido #{pedido.id}</p>
            <p className="text-xs text-ink-soft">{new Date(pedido.created_at).toLocaleString("es-AR")}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="font-mono tabular text-sm">${Number(pedido.total).toFixed(2)}</span>
            <EstadoPedidoBadge estado={pedido.estado_codigo} />
          </div>
        </button>
      ))}

      {totalPaginas > 1 && (
        <div className="flex items-center justify-center gap-3 pt-2">
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
    </div>
  );
}
