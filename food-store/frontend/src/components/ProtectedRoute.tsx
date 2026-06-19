import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import type { RolCodigo } from "../types";

interface ProtectedRouteProps {
  children: ReactNode;
  roles?: RolCodigo[];
}

export function ProtectedRoute({ children, roles }: ProtectedRouteProps) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const hasRole = useAuthStore((s) => s.hasRole);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  if (roles && roles.length > 0 && !hasRole(...roles)) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}
