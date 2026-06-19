import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { DollarSign, Users, Sandwich, TrendingUp } from "lucide-react";
import { useDashboard } from "../../hooks/useAdmin";
import { Skeleton } from "../../components/Skeleton";
import { ESTADO_LABEL } from "../../components/Badge";
import type { EstadoPedidoCodigo } from "../../types";

function KpiCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-line bg-surface p-4">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-mostaza-50 text-mostaza-600">
        {icon}
      </div>
      <div>
        <p className="text-xs text-ink-soft">{label}</p>
        <p className="font-display text-xl font-bold tabular">{value}</p>
      </div>
    </div>
  );
}

export function DashboardPage() {
  const { data, isLoading } = useDashboard();

  if (isLoading || !data) {
    return (
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-20" />
        ))}
      </div>
    );
  }

  const totalPedidos = Object.values(data.pedidos_por_estado).reduce((a, b) => a + b, 0);
  const chartData = Object.entries(data.pedidos_por_estado).map(([estado, cantidad]) => ({
    estado: ESTADO_LABEL[estado as EstadoPedidoCodigo],
    cantidad,
  }));

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <KpiCard icon={<DollarSign size={18} />} label="Ventas totales" value={`$${Number(data.total_ventas).toFixed(0)}`} />
        <KpiCard icon={<TrendingUp size={18} />} label="Pedidos" value={String(totalPedidos)} />
        <KpiCard icon={<Users size={18} />} label="Usuarios" value={String(data.total_usuarios)} />
        <KpiCard icon={<Sandwich size={18} />} label="Productos" value={String(data.total_productos)} />
      </div>

      <div className="rounded-2xl border border-line bg-surface p-5">
        <h2 className="mb-4 font-display font-semibold">Pedidos por estado</h2>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2D9C8" />
            <XAxis dataKey="estado" tick={{ fontSize: 12 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="cantidad" fill="#D98E04" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="rounded-2xl border border-line bg-surface p-5">
        <h2 className="mb-4 font-display font-semibold">Más vendidos</h2>
        {data.productos_mas_vendidos.length === 0 ? (
          <p className="text-sm text-ink-soft">Todavía no hay ventas confirmadas.</p>
        ) : (
          <ol className="flex flex-col gap-2">
            {data.productos_mas_vendidos.map((p, i) => (
              <li key={p.producto_id} className="flex items-center justify-between text-sm">
                <span>
                  <span className="mr-2 font-mono text-ink-soft">{i + 1}.</span>
                  {p.nombre}
                </span>
                <span className="font-mono tabular text-ink-soft">{p.cantidad_vendida} unidades</span>
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}
