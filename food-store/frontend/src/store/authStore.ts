import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { RolCodigo, TokenResponse, Usuario } from "../types";

interface AuthState {
  accessToken: string | null;
  // No persiste (ver partialize abajo): si se refresca la página y el
  // access token ya venció, se fuerza re-login en vez de refrescar en
  // silencio. Es una limitación conocida y aceptada del diseño (sección 9
  // de la spec solo pide persistir accessToken).
  refreshToken: string | null;
  usuario: Usuario | null;
  isAuthenticated: boolean;
  setAuth: (tokens: TokenResponse, usuario: Usuario) => void;
  setAccessToken: (token: string) => void;
  setUsuario: (usuario: Usuario) => void;
  logout: () => void;
  hasRole: (...roles: RolCodigo[]) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      usuario: null,
      isAuthenticated: false,

      setAuth: (tokens, usuario) =>
        set({
          accessToken: tokens.access_token,
          refreshToken: tokens.refresh_token,
          usuario,
          isAuthenticated: true,
        }),

      setAccessToken: (token) => set({ accessToken: token }),

      setUsuario: (usuario) => set({ usuario, isAuthenticated: true }),

      logout: () =>
        set({ accessToken: null, refreshToken: null, usuario: null, isAuthenticated: false }),

      hasRole: (...roles) => {
        const usuario = get().usuario;
        if (!usuario) return false;
        return roles.some((r) => usuario.roles.includes(r));
      },
    }),
    {
      name: "foodstore-auth",
      partialize: (state) => ({ accessToken: state.accessToken }),
    }
  )
);
