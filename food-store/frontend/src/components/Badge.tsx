import type { ReactNode } from "react";
import clsx from "clsx";
import type { EstadoPedidoCodigo } from "../types";

type Tone = "neutral" | "warning" | "success" | "danger" | "info";

const TONE_CLASSES: Record<Tone, string> = {
  neutral: "bg-ink/5 text-ink-soft",
  warning: "bg-mostaza-100 text-mostaza-700",
  success: "bg-oliva-50 text-oliva-600",
  danger: "bg-brasa-500/10 text-brasa-600",
  info: "bg-sky-100 text-sky-700",
};

export function Badge({ tone = "neutral", children }: { tone?: Tone; children: ReactNode }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold",
        TONE_CLASSES[tone]
      )}
    >
      {children}
    </span>
  );
}

const ESTADO_LABEL: Record<EstadoPedidoCodigo, string> = {
  PENDIENTE: "Pendiente",
  CONFIRMADO: "Confirmado",
  EN_PREPARACION: "En preparación",
  EN_CAMINO: "En camino",
  ENTREGADO: "Entregado",
  CANCELADO: "Cancelado",
};

const ESTADO_TONE: Record<EstadoPedidoCodigo, Tone> = {
  PENDIENTE: "warning",
  CONFIRMADO: "info",
  EN_PREPARACION: "info",
  EN_CAMINO: "info",
  ENTREGADO: "success",
  CANCELADO: "danger",
};

export function EstadoPedidoBadge({ estado }: { estado: EstadoPedidoCodigo }) {
  return <Badge tone={ESTADO_TONE[estado]}>{ESTADO_LABEL[estado]}</Badge>;
}

export { ESTADO_LABEL };
