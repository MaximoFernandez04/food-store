import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { direccionesApi, type DireccionData } from "../api/direccionesApi";

export function useDirecciones() {
  return useQuery({ queryKey: ["direcciones"], queryFn: direccionesApi.list });
}

export function useCreateDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: DireccionData) => direccionesApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["direcciones"] }),
  });
}

export function useUpdateDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<DireccionData> }) => direccionesApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["direcciones"] }),
  });
}

export function useSetDireccionPrincipal() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: direccionesApi.setPrincipal,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["direcciones"] }),
  });
}

export function useDeleteDireccion() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: direccionesApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["direcciones"] }),
  });
}
