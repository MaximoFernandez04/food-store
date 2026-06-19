import type { HistorialRead } from "../../types";
import { ESTADO_LABEL } from "../../components/Badge";

function formatHora(iso: string): string {
  return new Date(iso).toLocaleString("es-AR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
}

/**
 * El pedido de un restaurante es, literalmente, un ticket de cocina que
 * avanza por estados en secuencia — así que un timeline tipo "ticket"
 * perforado entre cada paso no es un adorno, es el objeto real que
 * representa. Cada corte punteado es una transición de HistorialEstadoPedido.
 */
export function HistorialTimeline({ historial }: { historial: HistorialRead[] }) {
  if (historial.length === 0) return null;

  return (
    <div className="rounded-2xl border border-line bg-surface p-1 shadow-ticket">
      <div className="rounded-xl bg-[repeating-linear-gradient(135deg,theme(colors.mostaza.50)_0px,theme(colors.mostaza.50)_10px,transparent_10px,transparent_20px)] p-0.5">
        <div className="rounded-xl bg-surface p-5">
          <ol>
            {historial.map((h, i) => {
              const esUltimo = i === historial.length - 1;
              const esCancelado = h.estado_hasta === "CANCELADO";
              return (
                <li key={h.id} className="relative pb-6 pl-8 last:pb-0">
                  {!esUltimo && (
                    <span
                      className="absolute left-[7px] top-3 bottom-0 w-px border-l border-dashed border-line"
                      aria-hidden="true"
                    />
                  )}
                  <span
                    className={`absolute left-0 top-1 flex h-4 w-4 items-center justify-center rounded-full ${
                      esCancelado ? "bg-brasa-500" : esUltimo ? "bg-mostaza-500" : "bg-oliva-500"
                    }`}
                    aria-hidden="true"
                  />
                  <p className="font-mono text-xs tabular text-ink-soft">{formatHora(h.created_at)}</p>
                  <p className="font-medium">{ESTADO_LABEL[h.estado_hasta]}</p>
                  {h.motivo && <p className="text-sm text-ink-soft">{h.motivo}</p>}
                  {h.usuario_id === null && <p className="text-xs text-ink-soft/70">Actualizado automáticamente</p>}
                </li>
              );
            })}
          </ol>
        </div>
      </div>
    </div>
  );
}
