import { PedidoList } from "../features/pedidos/PedidoList";

export function PedidosPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="mb-6 font-display text-3xl font-bold">Mis pedidos</h1>
      <PedidoList />
    </div>
  );
}
