import { NavLink, Outlet } from "react-router-dom";
import { LayoutDashboard, Tag, Sandwich, ClipboardList } from "lucide-react";
import clsx from "clsx";

const NAV_ITEMS = [
  { to: "/admin", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/admin/categorias", label: "Categorías", icon: Tag, end: false },
  { to: "/admin/productos", label: "Productos", icon: Sandwich, end: false },
  { to: "/admin/pedidos", label: "Pedidos", icon: ClipboardList, end: false },
];

export function AdminLayout() {
  return (
    <div className="mx-auto flex max-w-6xl gap-6 px-4 py-8">
      <aside className="w-48 shrink-0">
        <nav className="flex flex-col gap-1">
          {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                clsx(
                  "flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive ? "bg-ink text-paper" : "text-ink-soft hover:bg-ink/5"
                )
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  );
}
