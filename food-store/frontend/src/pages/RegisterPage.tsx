import { Link } from "react-router-dom";
import { RegisterForm } from "../features/auth/RegisterForm";

export function RegisterPage() {
  return (
    <div className="mx-auto flex max-w-md flex-col gap-6 px-4 py-16">
      <div className="text-center">
        <h1 className="font-display text-3xl font-bold">Creá tu cuenta</h1>
        <p className="mt-1 text-sm text-ink-soft">Pedí en minutos y seguí tus pedidos en vivo.</p>
      </div>
      <div className="rounded-2xl border border-line bg-surface p-6 shadow-ticket">
        <RegisterForm />
      </div>
      <p className="text-center text-sm text-ink-soft">
        ¿Ya tenés cuenta?{" "}
        <Link to="/login" className="font-semibold text-mostaza-600 hover:underline">
          Ingresá
        </Link>
      </p>
    </div>
  );
}
