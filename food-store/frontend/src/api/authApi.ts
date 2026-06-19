import { axiosClient } from "./axiosClient";
import type { TokenResponse, Usuario } from "../types";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  nombre: string;
  apellido: string;
  email: string;
  password: string;
}

export const authApi = {
  login: (data: LoginRequest) =>
    axiosClient.post<TokenResponse>("/api/v1/auth/login", data).then((r) => r.data),

  register: (data: RegisterRequest) =>
    axiosClient.post<Usuario>("/api/v1/auth/register", data).then((r) => r.data),

  me: () => axiosClient.get<Usuario>("/api/v1/auth/me").then((r) => r.data),

  logout: (refresh_token: string) => axiosClient.post("/api/v1/auth/logout", { refresh_token }),
};
