import { create } from "zustand";

interface ConfirmModalState {
  title: string;
  message: string;
  confirmLabel?: string;
  danger?: boolean;
  onConfirm: () => void;
}

interface UiState {
  cartOpen: boolean;
  sidebarOpen: boolean;
  confirmModal: ConfirmModalState | null;
  openCart: () => void;
  closeCart: () => void;
  toggleCart: () => void;
  toggleSidebar: () => void;
  openConfirmModal: (modal: ConfirmModalState) => void;
  closeConfirmModal: () => void;
}

export const useUiStore = create<UiState>((set) => ({
  cartOpen: false,
  sidebarOpen: false,
  confirmModal: null,

  openCart: () => set({ cartOpen: true }),
  closeCart: () => set({ cartOpen: false }),
  toggleCart: () => set((s) => ({ cartOpen: !s.cartOpen })),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  openConfirmModal: (modal) => set({ confirmModal: modal }),
  closeConfirmModal: () => set({ confirmModal: null }),
}));
