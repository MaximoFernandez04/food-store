import clsx from "clsx";

export function Skeleton({ className }: { className?: string }) {
  return <div className={clsx("animate-pulse rounded-md bg-ink/10", className)} />;
}

export function ProductCardSkeleton() {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-line bg-surface p-4">
      <Skeleton className="h-32 w-full rounded-xl" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-3 w-1/2" />
      <Skeleton className="h-9 w-full rounded-lg" />
    </div>
  );
}

export function RowSkeleton() {
  return <Skeleton className="h-14 w-full rounded-lg" />;
}
