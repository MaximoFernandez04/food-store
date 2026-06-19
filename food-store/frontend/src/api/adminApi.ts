import { axiosClient } from "./axiosClient";
import type { DashboardStats } from "../types";

export const adminApi = {
  dashboard: () => axiosClient.get<DashboardStats>("/api/v1/admin/dashboard").then((r) => r.data),
};
