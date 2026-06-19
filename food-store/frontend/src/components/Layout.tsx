import { Link, Outlet, useNavigate } from "react-router-dom";
import { ShoppingBag, ClipboardList, LogOut, UserCircle2 } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { useCartStore } from "../store/cartStore";
import { useUiStore } from "../store/uiStore";
import { useLogout } from "../hooks/useAuth";
import { CartDrawer } from "../features/cart/CartDrawer";

export function Layout() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const usuario = useAuthStore((s) => s.usuario);
  const hasRole = useAuthStore((s) => s.hasRole);
  const itemCount = useCartStore((s) => s.itemCount());
  const toggleCart = useUiStore((s) => s.toggleCart);
  const logout = useLogout();
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-30 border-b border-line bg-paper/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <Link to="/" className="font-display text-xl font-bold tracking-tight">
            Food<span className="text-mostaza-500">Store</span>
          </Link>

          <nav className="flex items-center gap-2">
            {isAuthenticated && (
              <button
                onClick={() => navigate("/pedidos")}
                className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-ink-soft hover:bg-ink/5"
              >
                <ClipboardList size={18} />
                <span className="hidden sm:inline">Mis pedidos</span>
              </button>
            )}

            {hasRole("ADMIN", "STOCK", "PEDIDOS") && (
              <Link
                to="/admin"
                className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-ink-soft hover:bg-ink/5"
              >
                Panel
              </Link>
            )}

            <button
              onClick={toggleCart}
              aria-label="Abrir carrito"
              className="relative flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-ink-soft hover:bg-ink/5"
            >
              <ShoppingBag size={18} />
              {itemCount > 0 && (
                <span className="absolute -right-0.5 -top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-mostaza-500 text-[11px] font-bold text-white">
                  {itemCount}
                </span>
              )}
            </button>

            {isAuthenticated ? (
              <div className="ml-1 flex items-center gap-2 border-l border-line pl-3">
                <span className="hidden items-center gap-1.5 text-sm text-ink-soft sm:flex">
                  <UserCircle2 size={18} />
                  {usuario?.nombre}
                </span>
                <button
                  onClick={logout}
                  aria-label="Cerrar sesión"
                  className="rounded-lg p-2 text-ink-soft hover:bg-ink/5"
                >
                  <LogOut size={18} />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="ml-1 rounded-lg bg-mostaza-500 px-4 py-2 text-sm font-semibold text-white hover:bg-mostaza-600"
              >
                Ingresar
              </Link>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <CartDrawer />

      <footer className="border-t border-line px-4 py-6 text-center text-xs text-ink-soft">
        Food Store — Trabajo Práctico Integrador, Programación 4
      </footer>
    </div>
  );
}
