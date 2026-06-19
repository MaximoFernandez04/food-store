import { create } from "zustand";
import type { MpEstadoPago } from "../types";

type PaymentStatus = "idle" | "processing" | "approved" | "rejected" | "error";

interface PaymentState {
  status: PaymentStatus;
  mpPaymentId: number | null;
  statusDetail: string | null;
  setProcessing: () => void;
  setResult: (mpStatus: MpEstadoPago, mpPaymentId: number | null, statusDetail: string | null) => void;
  setError: (detail: string) => void;
  reset: () => void;
}

function mapMpStatus(mpStatus: MpEstadoPago): PaymentStatus {
  if (mpStatus === "approved") return "approved";
  if (mpStatus === "rejected") return "rejected";
  return "processing"; // pending / in_process / cancelled: el webhook resuelve después
}

// Sin middleware persist: se resetea al recargar la página, a propósito
// (no tiene sentido conservar "estaba procesando un pago" entre sesiones).
export const usePaymentStore = create<PaymentState>((set) => ({
  status: "idle",
  mpPaymentId: null,
  statusDetail: null,

  setProcessing: () => set({ status: "processing", statusDetail: null }),

  setResult: (mpStatus, mpPaymentId, statusDetail) =>
    set({ status: mapMpStatus(mpStatus), mpPaymentId, statusDetail }),

  setError: (detail) => set({ status: "error", statusDetail: detail }),

  reset: () => set({ status: "idle", mpPaymentId: null, statusDetail: null }),
}));
