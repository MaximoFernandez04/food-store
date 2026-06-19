import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ingredientesApi, productosApi, type ProductosFiltro, type ProductoUpdateData } from "../api/productosApi";
import type { ProductoCreateData } from "../api/productosApi";

export function useProductos(filtro: ProductosFiltro) {
  return useQuery({
    queryKey: ["productos", filtro],
    queryFn: () => productosApi.list(filtro),
    placeholderData: (prev) => prev, // evita parpadeo blanco al paginar/filtrar
  });
}

export function useProducto(id: number | null) {
  return useQuery({
    queryKey: ["productos", id],
    queryFn: () => productosApi.get(id as number),
    enabled: id !== null,
  });
}

export function useCreateProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ProductoCreateData) => productosApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });
}

export function useUpdateProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductoUpdateData }) => productosApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });
}

export function useSetDisponibilidad() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, disponible }: { id: number; disponible: boolean }) =>
      productosApi.setDisponibilidad(id, disponible),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });
}

export function useSetStock() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, stock_cantidad }: { id: number; stock_cantidad: number }) =>
      productosApi.setStock(id, stock_cantidad),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });
}

export function useDeleteProducto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: productosApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });
}

export function useIngredientes() {
  return useQuery({ queryKey: ["ingredientes"], queryFn: ingredientesApi.list });
}

export function useCreateIngrediente() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ingredientesApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredientes"] }),
  });
}
