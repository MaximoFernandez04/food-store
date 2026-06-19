import { type ReactNode, useEffect } from "react";
import { X } from "lucide-react";
import { useUiStore } from "../store/uiStore";
import { Button } from "./Button";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  maxWidth?: string;
}

export function Modal({ open, onClose, title, children, maxWidth = "max-w-lg" }: ModalProps) {
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-ink/40" onClick={onClose} aria-hidden="true" />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className={`relative z-10 w-full ${maxWidth} max-h-[90vh] overflow-y-auto rounded-2xl bg-surface p-6 shadow-ticket`}
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 id="modal-title" className="text-lg font-display font-semibold">
            {title}
          </h2>
          <button
            onClick={onClose}
            aria-label="Cerrar"
            className="rounded-full p-1.5 text-ink-soft hover:bg-ink/5"
          >
            <X size={18} />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

/** Confirmación genérica (cancelar pedido, borrar producto, etc.) — vive
 * una sola vez en App.tsx y se dispara desde cualquier lado con
 * useUiStore.openConfirmModal(). */
export function GlobalConfirmModal() {
  const confirmModal = useUiStore((s) => s.confirmModal);
  const closeConfirmModal = useUiStore((s) => s.closeConfirmModal);

  if (!confirmModal) return null;

  return (
    <Modal open onClose={closeConfirmModal} title={confirmModal.title} maxWidth="max-w-md">
      <p className="text-sm text-ink-soft">{confirmModal.message}</p>
      <div className="mt-6 flex justify-end gap-3">
        <Button variant="ghost" onClick={closeConfirmModal}>
          Cancelar
        </Button>
        <Button
          variant={confirmModal.danger ? "danger" : "primary"}
          onClick={() => {
            confirmModal.onConfirm();
            closeConfirmModal();
          }}
        >
          {confirmModal.confirmLabel ?? "Confirmar"}
        </Button>
      </div>
    </Modal>
  );
}
