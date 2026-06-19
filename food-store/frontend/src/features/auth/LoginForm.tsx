import { Link } from "react-router-dom";
import { useForm } from "@tanstack/react-form";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { useLogin } from "../../hooks/useAuth";
import { getApiErrorMessage } from "../../api/axiosClient";

export function LoginForm() {
  const login = useLogin();

  const form = useForm({
    defaultValues: { email: "", password: "" },
    onSubmit: async ({ value }) => {
      await login.mutateAsync(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
      className="flex flex-col gap-4"
    >
      <form.Field
        name="email"
        validators={{
          onChange: ({ value }) => (!value ? "El email es obligatorio" : undefined),
        }}
      >
        {(field) => (
          <Input
            label="Email"
            type="email"
            name={field.name}
            value={field.state.value}
            onBlur={field.handleBlur}
            onChange={(e) => field.handleChange(e.target.value)}
            error={field.state.meta.errors[0] as string | undefined}
            autoComplete="email"
          />
        )}
      </form.Field>

      <form.Field
        name="password"
        validators={{
          onChange: ({ value }) => (!value ? "La contraseña es obligatoria" : undefined),
        }}
      >
        {(field) => (
          <Input
            label="Contraseña"
            type="password"
            name={field.name}
            value={field.state.value}
            onBlur={field.handleBlur}
            onChange={(e) => field.handleChange(e.target.value)}
            error={field.state.meta.errors[0] as string | undefined}
            autoComplete="current-password"
          />
        )}
      </form.Field>

      {login.isError && (
        <p className="rounded-lg bg-brasa-500/10 px-3 py-2 text-sm text-brasa-600">
          {getApiErrorMessage(login.error)}
        </p>
      )}

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting] as const}>
        {([canSubmit, isSubmitting]) => (
          <Button type="submit" disabled={!canSubmit} loading={isSubmitting || login.isPending} size="lg">
            Ingresar
          </Button>
        )}
      </form.Subscribe>

      <p className="text-center text-sm text-ink-soft">
        ¿No tenés cuenta?{" "}
        <Link to="/register" className="font-semibold text-mostaza-600 hover:underline">
          Registrate
        </Link>
      </p>
    </form>
  );
}
