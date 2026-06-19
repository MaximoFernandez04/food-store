import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { CartItem } from "../types";

// Mismo valor fijo que app/modules/pedidos/service.py::COSTO_ENVIO_FIJO.
// Es solo para mostrar un total estimado en el carrito — el backend
// vuelve a calcular todo (subtotal, envío, total) al crear el pedido y
// esa es la fuente de verdad real, no este store.
const COSTO_ENVIO_ESTIMADO = 50;

function mismaPersonalizacion(a: number[], b: number[]): boolean {
  if (a.length !== b.length) return false;
  const sa = [...a].sort();
  const sb = [...b].sort();
  return sa.every((v, i) => v === sb[i]);
}

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (producto_id: number, personalizacion: number[]) => void;
  updateCantidad: (producto_id: number, personalizacion: number[], cantidad: number) => void;
  clearCart: () => void;
  itemCount: () => number;
  subtotal: () => number;
  costoEnvio: () => number;
  total: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) =>
        set((state) => {
          const existente = state.items.find(
            (i) =>
              i.producto_id === item.producto_id &&
              mismaPersonalizacion(i.personalizacion, item.personalizacion)
          );
          if (existente) {
            return {
              items: state.items.map((i) =>
                i === existente ? { ...i, cantidad: i.cantidad + item.cantidad } : i
              ),
            };
          }
          return { items: [...state.items, item] };
        }),

      removeItem: (producto_id, personalizacion) =>
        set((state) => ({
          items: state.items.filter(
            (i) => !(i.producto_id === producto_id && mismaPersonalizacion(i.personalizacion, personalizacion))
          ),
        })),

      updateCantidad: (producto_id, personalizacion, cantidad) =>
        set((state) => ({
          items: state.items
            .map((i) =>
              i.producto_id === producto_id && mismaPersonalizacion(i.personalizacion, personalizacion)
                ? { ...i, cantidad }
                : i
            )
            .filter((i) => i.cantidad > 0),
        })),

      clearCart: () => set({ items: [] }),

      itemCount: () => get().items.reduce((acc, i) => acc + i.cantidad, 0),

      subtotal: () => get().items.reduce((acc, i) => acc + i.precio_base * i.cantidad, 0),

      costoEnvio: () => (get().items.length > 0 ? COSTO_ENVIO_ESTIMADO : 0),

      total: () => get().subtotal() + get().costoEnvio(),
    }),
    { name: "foodstore-cart" }
  )
);
