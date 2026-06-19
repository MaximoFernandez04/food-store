import { CardPayment } from "@mercadopago/sdk-react";
import { useCrearPago } from "../../hooks/usePagos";
import { usePaymentStore } from "../../store/paymentStore";
import { useToast } from "../../components/Toast";
import type { PagoResponse } from "../../types";

interface CardPaymentFormProps {
  pedidoId: number;
  amount: number;
  payerEmail: string;
  onResultado: (pago: PagoResponse) => void;
}

export function CardPaymentForm({ pedidoId, amount, payerEmail, onResultado }: CardPaymentFormProps) {
  const crearPago = useCrearPago();
  const setProcessing = usePaymentStore((s) => s.setProcessing);
  const setResult = usePaymentStore((s) => s.setResult);
  const setError = usePaymentStore((s) => s.setError);
  const toast = useToast();

  return (
    <CardPayment
      initialization={{ amount, payer: { email: payerEmail } }}
      locale="es-AR"
      onSubmit={async (formData) => {
        setProcessing();
        try {
          const pago = await crearPago.mutateAsync({
            pedido_id: pedidoId,
            token: formData.token,
            payer_email: formData.payer.email || payerEmail,
            installments: formData.installments,
          });
          setResult(pago.mp_status, pago.mp_payment_id, pago.mp_status_detail);
          onResultado(pago);
        } catch (err) {
          setError("No pudimos procesar el pago. Probá con otra tarjeta.");
          toast.show("El pago no pudo procesarse", "error");
          throw err; // el Brick necesita que rechace para mostrar su propio error
        }
      }}
      onError={() => {
        toast.show("Revisá los datos de la tarjeta", "error");
      }}
    />
  );
}
