import { useQuery } from "@tanstack/react-query";
import { adminApi } from "../api/adminApi";

export function useDashboard() {
  return useQuery({ queryKey: ["admin", "dashboard"], queryFn: adminApi.dashboard });
}
