import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../store/authStore";
import type { ApiErrorBody, TokenResponse } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export const axiosClient = axios.create({ baseURL: API_URL });

// --- Request: agrega el Bearer token (acceso al store fuera de React) ---
axiosClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Response: si el access token venció (401), intenta refrescar UNA
// vez y reintenta la request original. Si el refresh también falla,
// desloguea. Las requests concurrentes comparten la misma promesa de
// refresh para no disparar N refreshes en paralelo. ---
let refreshPromise: Promise<string> | null = null;

interface RetriableConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

async function refrescarAccessToken(): Promise<string> {
  const refreshToken = useAuthStore.getState().refreshToken;
  if (!refreshToken) {
    throw new Error("No hay refresh token disponible");
  }
  const { data } = await axios.post<TokenResponse>(`${API_URL}/api/v1/auth/refresh`, {
    refresh_token: refreshToken,
  });
  useAuthStore.getState().setAccessToken(data.access_token);
  return data.access_token;
}

axiosClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetriableConfig | undefined;

    if (error.response?.status === 401 && config && !config._retry) {
      config._retry = true;
      try {
        refreshPromise ??= refrescarAccessToken().finally(() => {
          refreshPromise = null;
        });
        const nuevoToken = await refreshPromise;
        config.headers.Authorization = `Bearer ${nuevoToken}`;
        return axiosClient(config);
      } catch {
        useAuthStore.getState().logout();
        window.location.href = "/login";
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

/** Extrae un mensaje legible del error RFC-7807-ish que devuelve el backend. */
export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const body = error.response?.data as ApiErrorBody | undefined;
    if (body?.detail) return body.detail;
  }
  return "Ocurrió un error inesperado. Intentá de nuevo.";
}

export function getApiErrorCode(error: unknown): string | null {
  if (axios.isAxiosError(error)) {
    const body = error.response?.data as ApiErrorBody | undefined;
    return body?.code ?? null;
  }
  return null;
}
