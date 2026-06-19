import { LoginForm } from "../features/auth/LoginForm";

export function LoginPage() {
  return (
    <div className="mx-auto flex max-w-md flex-col gap-6 px-4 py-16">
      <div className="text-center">
        <h1 className="font-display text-3xl font-bold">Bienvenido de nuevo</h1>
        <p className="mt-1 text-sm text-ink-soft">Ingresá para pedir y seguir tus pedidos.</p>
      </div>
      <div className="rounded-2xl border border-line bg-surface p-6 shadow-ticket">
        <LoginForm />
      </div>
    </div>
  );
}
