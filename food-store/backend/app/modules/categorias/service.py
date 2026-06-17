from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import CategoriaCreate, CategoriaUpdate


def create_categoria(uow: UnitOfWork, data: CategoriaCreate) -> Categoria:
    if data.parent_id is not None and not uow.categorias.get_by_id(data.parent_id):
        raise AppError(
            status_code=404,
            detail=f"La categoría padre {data.parent_id} no existe",
            code="PARENT_NOT_FOUND",
            field="parent_id",
        )
    categoria = Categoria(nombre=data.nombre, parent_id=data.parent_id)
    return uow.categorias.create(categoria)


def update_categoria(uow: UnitOfWork, categoria_id: int, data: CategoriaUpdate) -> Categoria:
    categoria = uow.categorias.get_by_id(categoria_id)
    if not categoria:
        raise AppError(404, "Categoría no encontrada", "NOT_FOUND")

    if data.parent_id is not None and data.parent_id == categoria_id:
        raise AppError(
            400, "Una categoría no puede ser su propia padre", "INVALID_PARENT", "parent_id"
        )

    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(categoria, key, value)
    return uow.categorias.update(categoria)


def soft_delete_categoria(uow: UnitOfWork, categoria_id: int) -> None:
    categoria = uow.categorias.get_by_id(categoria_id)
    if not categoria:
        raise AppError(404, "Categoría no encontrada", "NOT_FOUND")

    if uow.categorias.has_hijos_activos(categoria_id):
        raise AppError(
            400,
            "No se puede eliminar: tiene subcategorías activas",
            "HAS_CHILDREN",
        )

    if uow.productos.has_productos_activos(categoria_id):
        raise AppError(
            400,
            "No se puede eliminar: tiene productos activos asociados",
            "HAS_PRODUCTS",
        )

    uow.categorias.soft_delete(categoria)
