import { useForm } from "@tanstack/react-form";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { useCreateDireccion } from "../../hooks/useDirecciones";

export function DireccionForm({ onCreated }: { onCreated: () => void }) {
  const crear = useCreateDireccion();

  const form = useForm({
    defaultValues: { alias: "", linea1: "", linea2: "" },
    onSubmit: async ({ value }) => {
      await crear.mutateAsync({
        alias: value.alias || null,
        linea1: value.linea1,
        linea2: value.linea2 || null,
      });
      onCreated();
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
      className="flex flex-col gap-3"
    >
      <form.Field name="alias">
        {(field) => (
          <Input
            label="Nombre de la dirección (opcional)"
            placeholder="Casa, trabajo…"
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
          />
        )}
      </form.Field>

      <form.Field
        name="linea1"
        validators={{ onChange: ({ value }) => (value.length < 3 ? "Ingresá la dirección" : undefined) }}
      >
        {(field) => (
          <Input
            label="Calle y número"
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
            onBlur={field.handleBlur}
            error={field.state.meta.errors[0] as string | undefined}
          />
        )}
      </form.Field>

      <form.Field name="linea2">
        {(field) => (
          <Input
            label="Piso / depto / entre calles (opcional)"
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
          />
        )}
      </form.Field>

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting] as const}>
        {([canSubmit, isSubmitting]) => (
          <Button type="submit" disabled={!canSubmit} loading={isSubmitting || crear.isPending}>
            Guardar dirección
          </Button>
        )}
      </form.Subscribe>
    </form>
  );
}
