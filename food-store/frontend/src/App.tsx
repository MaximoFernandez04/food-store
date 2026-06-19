import { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { GlobalConfirmModal } from "./components/Modal";
import { useAuthStore } from "./store/authStore";
import { useMe } from "./hooks/useAuth";
import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { CheckoutPage } from "./pages/CheckoutPage";
import { PedidosPage } from "./pages/PedidosPage";
import { PedidoDetailPage } from "./pages/PedidoDetailPage";
import { AdminLayout } from "./features/admin/AdminLayout";
import { DashboardPage } from "./features/admin/DashboardPage";
import { CategoriasAdminPage } from "./features/admin/CategoriasAdminPage";
import { ProductosAdminPage } from "./features/admin/ProductosAdminPage";
import { PedidosAdminPage } from "./features/admin/PedidosAdminPage";

export function App() {
  // authStore solo persiste el accessToken (sección 9 de la spec). Al
  // recargar la página, isAuthenticated/usuario arrancan en null/false —
  // este efecto los reconstruye con GET /auth/me si hay token guardado.
  const accessToken = useAuthStore((s) => s.accessToken);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const setUsuario = useAuthStore((s) => s.setUsuario);
  const logout = useAuthStore((s) => s.logout);
  const { data: usuarioRehidratado, isError } = useMe(!!accessToken && !isAuthenticated);

  useEffect(() => {
    if (usuarioRehidratado) setUsuario(usuarioRehidratado);
  }, [usuarioRehidratado, setUsuario]);

  useEffect(() => {
    // El access token persistido ya no es válido y no se pudo refrescar
    // (sin refreshToken en memoria tras el reload) -> fuerza re-login.
    if (isError) logout();
  }, [isError, logout]);

  return (
    <>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/checkout"
            element={
              <ProtectedRoute>
                <CheckoutPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/pedidos"
            element={
              <ProtectedRoute>
                <PedidosPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/pedidos/:id"
            element={
              <ProtectedRoute>
                <PedidoDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute roles={["ADMIN", "STOCK", "PEDIDOS"]}>
                <AdminLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="categorias" element={<CategoriasAdminPage />} />
            <Route path="productos" element={<ProductosAdminPage />} />
            <Route path="pedidos" element={<PedidosAdminPage />} />
          </Route>
        </Route>
      </Routes>
      <GlobalConfirmModal />
    </>
  );
}
