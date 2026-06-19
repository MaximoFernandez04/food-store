import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { initMercadoPago } from "@mercadopago/sdk-react";
import { App } from "./App";
import { ToastProvider } from "./components/Toast";
import "./index.css";

// Se inicializa una sola vez, a nivel módulo (no en cada render).
if (import.meta.env.VITE_MP_PUBLIC_KEY) {
  initMercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY, { locale: "es-AR" });
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ToastProvider>
          <App />
        </ToastProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
);
