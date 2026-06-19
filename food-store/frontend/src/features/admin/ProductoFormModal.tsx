import { useState } from "react";
import { useForm } from "@tanstack/react-form";
import { Modal } from "../../components/Modal";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Skeleton } from "../../components/Skeleton";
import { useCategorias } from "../../hooks/useCategorias";
import { useIngredientes, useCreateProducto, useUpdateProducto, useProducto } from "../../hooks/useProductos";
import { useToast } from "../../components/Toast";
import { getApiErrorMessage } from "../../api/axiosClient";
import type { ProductoDetail } from "../../types";

interface ProductoFormModalProps {
  productoId: number | null; // null = alta
  onClose: () => void;
}

export function ProductoFormModal({ productoId, onClose }: ProductoFormModalProps) {
  const esEdicion = productoId !== null;
  const { data: productoActual, isLoading } = useProducto(productoId);

  return (
    <Modal open onClose={onClose} title={esEdicion ? "Editar producto" : "Nuevo producto"} maxWidth="max-w-xl">
      {esEdicion && isLoading ? (
        <div className="flex flex-col gap-3">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
        </div>
      ) : (
        // Se monta UNA VEZ que productoActual ya está listo (o de una en alta),
        // así useForm captura los defaultValues correctos desde el primer
        // render — TanStack Form no re-lee defaultValues si llegan después.
        <ProductoFormFields producto={productoActual ?? null} onDone={onClose} />
      )}
    </Modal>
  );
}

function ProductoFormFields({ producto, onDone }: { producto: ProductoDetail | null; onDone: () => void }) {
  const { data: categorias } = useCategorias();
  const { data: ingredientes } = useIngredientes();
  const crear = useCreateProducto();
  const actualizar = useUpdateProducto();
  const toast = useToast();

  const [categoriaIds, setCategoriaIds] = useState<number[]>(producto?.categorias.map((c) => c.id) ?? []);
  const [ingredienteIds, setIngredienteIds] = useState<number[]>(producto?.ingredientes.map((i) => i.id) ?? []);

  const form = useForm({
    defaultValues: {
      nombre: producto?.nombre ?? "",
      descripcion: producto?.descripcion ?? "",
      precio_base: producto ? Number(producto.precio_base) : 0,
      stock_cantidad: producto?.stock_cantidad ?? 0,
    },
    onSubmit: async ({ value }) => {
      try {
        if (producto) {
          await actualizar.mutateAsync({
            id: producto.id,
            data: { ...value, categoria_ids: categoriaIds, ingrediente_ids: ingredienteIds },
          });
          toast.show("Producto actualizado", "success");
        } else {
          await crear.mutateAsync({ ...value, categoria_ids: categoriaIds, ingrediente_ids: ingredienteIds });
          toast.show("Producto creado", "success");
        }
        onDone();
      } catch (err) {
        toast.show(getApiErrorMessage(err), "error");
      }
    },
  });

  const toggle = (list: number[], setList: (v: number[]) => void, id: number) =>
    setList(list.includes(id) ? list.filter((i) => i !== id) : [...list, id]);

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
        name="nombre"
        validators={{ onChange: ({ value }) => (value.length < 2 ? "Ingresá un nombre" : undefined) }}
      >
        {(field) => (
          <Input
            label="Nombre"
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
            error={field.state.meta.errors[0] as string | undefined}
          />
        )}
      </form.Field>

      <form.Field name="descripcion">
        {(field) => (
          <Input
            label="Descripción (opcional)"
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
          />
        )}
      </form.Field>

      <div className="grid grid-cols-2 gap-3">
        <form.Field
          name="precio_base"
          validators={{ onChange: ({ value }) => (value <= 0 ? "Tiene que ser mayor a 0" : undefined) }}
        >
          {(field) => (
            <Input
              label="Precio"
              type="number"
              step="0.01"
              value={field.state.value}
              onChange={(e) => field.handleChange(Number(e.target.value))}
              error={field.state.meta.errors[0] as string | undefined}
            />
          )}
        </form.Field>

        <form.Field
          name="stock_cantidad"
          validators={{ onChange: ({ value }) => (value < 0 ? "No puede ser negativo" : undefined) }}
        >
          {(field) => (
            <Input
              label="Stock"
              type="number"
              value={field.state.value}
              onChange={(e) => field.handleChange(Number(e.target.value))}
              error={field.state.meta.errors[0] as string | undefined}
            />
          )}
        </form.Field>
      </div>

      {categorias && categorias.length > 0 && (
        <div>
          <p className="mb-1.5 text-sm font-medium text-ink-soft">Categorías</p>
          <div className="flex flex-wrap gap-2">
            {categorias.map((cat) => (
              <button
                type="button"
                key={cat.id}
                onClick={() => toggle(categoriaIds, setCategoriaIds, cat.id)}
                className={`rounded-full px-3 py-1 text-xs font-medium ${
                  categoriaIds.includes(cat.id) ? "bg-ink text-paper" : "bg-ink/5 text-ink-soft"
                }`}
              >
                {cat.nombre}
              </button>
            ))}
          </div>
        </div>
      )}

      {ingredientes && ingredientes.length > 0 && (
        <div>
          <p className="mb-1.5 text-sm font-medium text-ink-soft">Ingredientes</p>
          <div className="flex flex-wrap gap-2">
            {ingredientes.map((ing) => (
              <button
                type="button"
                key={ing.id}
                onClick={() => toggle(ingredienteIds, setIngredienteIds, ing.id)}
                className={`rounded-full px-3 py-1 text-xs font-medium ${
                  ingredienteIds.includes(ing.id) ? "bg-ink text-paper" : "bg-ink/5 text-ink-soft"
                }`}
              >
                {ing.nombre}
              </button>
            ))}
          </div>
        </div>
      )}

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting] as const}>
        {([canSubmit, isSubmitting]) => (
          <Button type="submit" disabled={!canSubmit} loading={isSubmitting || crear.isPending || actualizar.isPending}>
            {producto ? "Guardar cambios" : "Crear producto"}
          </Button>
        )}
      </form.Subscribe>
    </form>
  );
}
