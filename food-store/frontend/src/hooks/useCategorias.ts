import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { categoriasApi } from "../api/categoriasApi";

export function useCategorias() {
  return useQuery({ queryKey: ["categorias"], queryFn: categoriasApi.list });
}

export function useCreateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: categoriasApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["categorias"] }),
  });
}

export function useUpdateCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: { nombre: string; parent_id?: number | null } }) =>
      categoriasApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["categorias"] }),
  });
}

export function useDeleteCategoria() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: categoriasApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["categorias"] }),
  });
}
