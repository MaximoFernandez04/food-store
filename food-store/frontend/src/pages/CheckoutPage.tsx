import { CheckoutForm } from "../features/checkout/CheckoutForm";

export function CheckoutPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="mb-6 font-display text-3xl font-bold">Finalizar pedido</h1>
      <CheckoutForm />
    </div>
  );
}
