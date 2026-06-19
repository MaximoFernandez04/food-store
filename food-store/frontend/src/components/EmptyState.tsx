import type { ReactNode } from "react";

export function EmptyState({
  icon,
  title,
  description,
  action,
}: {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-line px-6 py-16 text-center">
      {icon && <div className="text-ink-soft/50">{icon}</div>}
      <h3 className="font-display text-lg font-semibold">{title}</h3>
      {description && <p className="max-w-sm text-sm text-ink-soft">{description}</p>}
      {action}
    </div>
  );
}
