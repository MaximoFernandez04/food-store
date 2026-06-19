import { useNavigate } from "react-router-dom";
import { useForm } from "@tanstack/react-form";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { useRegister } from "../../hooks/useAuth";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";

export function RegisterForm() {
  const register = useRegister();
  const navigate = useNavigate();
  const toast = useToast();

  const form = useForm({
    defaultValues: { nombre: "", apellido: "", email: "", password: "" },
    onSubmit: async ({ value }) => {
      await register.mutateAsync(value);
      toast.show("Cuenta creada. Ya podés ingresar.", "success");
      navigate("/login");
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
      <div className="grid grid-cols-2 gap-3">
        <form.Field
          name="nombre"
          validators={{ onChange: ({ value }) => (value.length < 2 ? "Mínimo 2 caracteres" : undefined) }}
        >
          {(field) => (
            <Input
              label="Nombre"
              name={field.name}
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
              error={field.state.meta.errors[0] as string | undefined}
            />
          )}
        </form.Field>

        <form.Field
          name="apellido"
          validators={{ onChange: ({ value }) => (value.length < 2 ? "Mínimo 2 caracteres" : undefined) }}
        >
          {(field) => (
            <Input
              label="Apellido"
              name={field.name}
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
              error={field.state.meta.errors[0] as string | undefined}
            />
          )}
        </form.Field>
      </div>

      <form.Field
        name="email"
        validators={{ onChange: ({ value }) => (!value.includes("@") ? "Email inválido" : undefined) }}
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
          onChange: ({ value }) => (value.length < 8 ? "Mínimo 8 caracteres" : undefined),
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
            autoComplete="new-password"
          />
        )}
      </form.Field>

      {register.isError && (
        <p className="rounded-lg bg-brasa-500/10 px-3 py-2 text-sm text-brasa-600">
          {getApiErrorMessage(register.error)}
        </p>
      )}

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting] as const}>
        {([canSubmit, isSubmitting]) => (
          <Button type="submit" disabled={!canSubmit} loading={isSubmitting || register.isPending} size="lg">
            Crear cuenta
          </Button>
        )}
      </form.Subscribe>
    </form>
  );
}
