from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.productos.model import Producto
from app.modules.productos.schema import ProductoCreate, ProductoUpdate


def create_producto(uow: UnitOfWork, data: ProductoCreate) -> Producto:
    if uow.productos.get_by_nombre(data.nombre):
        raise AppError(400, "Ya existe un producto con ese nombre", "DUPLICATE_NAME", "nombre")

    for cat_id in data.categoria_ids:
        if not uow.categorias.get_by_id(cat_id):
            raise AppError(404, f"Categoría {cat_id} no existe", "CATEGORIA_NOT_FOUND")
    for ing_id in data.ingrediente_ids:
        if not uow.ingredientes.get_by_id(ing_id):
            raise AppError(404, f"Ingrediente {ing_id} no existe", "INGREDIENTE_NOT_FOUND")

    producto = Producto(
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio_base=data.precio_base,
        stock_cantidad=data.stock_cantidad,
    )
    uow.productos.create(producto)

    for i, cat_id in enumerate(data.categoria_ids):
        uow.productos.asignar_categoria(producto.id, cat_id, es_principal=(i == 0))
    for ing_id in data.ingrediente_ids:
        uow.productos.asignar_ingrediente(producto.id, ing_id)

    return producto


def update_producto(uow: UnitOfWork, producto_id: int, data: ProductoUpdate) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise AppError(404, "Producto no encontrado", "NOT_FOUND")

    updates = data.model_dump(exclude_unset=True)
    # categoria_ids/ingrediente_ids no son columnas de Producto: son
    # relaciones M:N que se manejan aparte (reemplazo completo del set).
    nuevas_categorias = updates.pop("categoria_ids", None)
    nuevos_ingredientes = updates.pop("ingrediente_ids", None)

    for key, value in updates.items():
        setattr(producto, key, value)
    uow.productos.update(producto)

    if nuevas_categorias is not None:
        for cat_id in nuevas_categorias:
            if not uow.categorias.get_by_id(cat_id):
                raise AppError(404, f"Categoría {cat_id} no existe", "CATEGORIA_NOT_FOUND")
        actuales = {c.id for c in uow.productos.categorias_de(producto.id)}
        for cat_id in actuales - set(nuevas_categorias):
            uow.productos.quitar_categoria(producto.id, cat_id)
        for i, cat_id in enumerate(c for c in nuevas_categorias if c not in actuales):
            uow.productos.asignar_categoria(producto.id, cat_id, es_principal=(i == 0 and not actuales))

    if nuevos_ingredientes is not None:
        for ing_id in nuevos_ingredientes:
            if not uow.ingredientes.get_by_id(ing_id):
                raise AppError(404, f"Ingrediente {ing_id} no existe", "INGREDIENTE_NOT_FOUND")
        actuales_ing = {i.id for i in uow.productos.ingredientes_de(producto.id)}
        for ing_id in actuales_ing - set(nuevos_ingredientes):
            uow.productos.quitar_ingrediente(producto.id, ing_id)
        for ing_id in set(nuevos_ingredientes) - actuales_ing:
            uow.productos.asignar_ingrediente(producto.id, ing_id)

    return producto


def set_disponibilidad(uow: UnitOfWork, producto_id: int, disponible: bool) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise AppError(404, "Producto no encontrado", "NOT_FOUND")
    producto.disponible = disponible
    return uow.productos.update(producto)


def set_stock(uow: UnitOfWork, producto_id: int, stock_cantidad: int) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise AppError(404, "Producto no encontrado", "NOT_FOUND")
    producto.stock_cantidad = stock_cantidad
    return uow.productos.update(producto)


def soft_delete_producto(uow: UnitOfWork, producto_id: int) -> None:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise AppError(404, "Producto no encontrado", "NOT_FOUND")
    uow.productos.soft_delete(producto)
