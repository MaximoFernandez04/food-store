import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { authApi, type LoginRequest, type RegisterRequest } from "../api/authApi";
import { useAuthStore } from "../store/authStore";
import { useCartStore } from "../store/cartStore";

export function useMe(enabled: boolean) {
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.me,
    enabled,
    retry: false,
  });
}

export function useLogin() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: async (tokens) => {
      // Necesitamos el usuario (roles incluidos) para el RBAC del lado del
      // cliente. authApi.me() ya manda el Bearer porque setAccessToken
      // ocurre antes que cualquier request gracias al interceptor leer
      // siempre del store en el momento de la request.
      useAuthStore.getState().setAccessToken(tokens.access_token);
      const usuario = await authApi.me();
      setAuth(tokens, usuario);
      queryClient.invalidateQueries({ queryKey: ["auth"] });
      const esStaff = usuario.roles.some((r) => r !== "CLIENT");
      navigate(esStaff ? "/admin" : "/");
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterRequest) => authApi.register(data),
  });
}

export function useLogout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return () => {
    const refreshToken = useAuthStore.getState().refreshToken;
    if (refreshToken) {
      authApi.logout(refreshToken).catch(() => {
        /* best-effort: si falla, igual desloguea localmente */
      });
    }
    useAuthStore.getState().logout();
    useCartStore.getState().clearCart();
    queryClient.clear();
    navigate("/login");
  };
}
