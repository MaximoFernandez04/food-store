from fastapi import APIRouter, Depends, Query, status

from app.core.deps import require_role
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.productos import service
from app.modules.productos.schema import (
    DisponibilidadUpdate,
    IngredienteCreate,
    IngredienteRead,
    PaginatedProductos,
    ProductoCreate,
    ProductoDetail,
    ProductoRead,
    ProductoUpdate,
    StockUpdate,
)

router = APIRouter(prefix="/api/v1/productos", tags=["productos"])

ROLES_GESTION = ["ADMIN", "STOCK"]


@router.get("", response_model=PaginatedProductos)
def list_productos(
    categoria: int | None = None,
    disponible: bool | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
):
    with UnitOfWork() as uow:
        items, total = uow.productos.search(categoria, disponible, search, page, size)
        return PaginatedProductos(items=items, total=total, page=page, size=size)


@router.get("/{producto_id}", response_model=ProductoDetail)
def get_producto(producto_id: int):
    with UnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        if not producto:
            raise AppError(404, f"Producto {producto_id} no encontrado", "NOT_FOUND")
        ingredientes = uow.productos.ingredientes_de(producto_id)
        categorias = uow.productos.categorias_de(producto_id)
        return ProductoDetail(**producto.model_dump(), ingredientes=ingredientes, categorias=categorias)


@router.post("", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        return service.create_producto(uow, data)


@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(
    producto_id: int, data: ProductoUpdate, _=Depends(require_role(["ADMIN"]))
):
    with UnitOfWork() as uow:
        return service.update_producto(uow, producto_id, data)


@router.patch("/{producto_id}/disponibilidad", response_model=ProductoRead)
def update_disponibilidad(
    producto_id: int, data: DisponibilidadUpdate, _=Depends(require_role(ROLES_GESTION))
):
    with UnitOfWork() as uow:
        return service.set_disponibilidad(uow, producto_id, data.disponible)


@router.patch("/{producto_id}/stock", response_model=ProductoRead)
def update_stock(
    producto_id: int, data: StockUpdate, _=Depends(require_role(ROLES_GESTION))
):
    with UnitOfWork() as uow:
        return service.set_stock(uow, producto_id, data.stock_cantidad)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        service.soft_delete_producto(uow, producto_id)


@router.get("/{producto_id}/ingredientes", response_model=list[IngredienteRead])
def list_ingredientes_producto(producto_id: int):
    with UnitOfWork() as uow:
        return uow.productos.ingredientes_de(producto_id)


@router.post(
    "/{producto_id}/ingredientes/{ingrediente_id}",
    status_code=status.HTTP_201_CREATED,
)
def asignar_ingrediente(
    producto_id: int, ingrediente_id: int, _=Depends(require_role(["ADMIN"]))
):
    with UnitOfWork() as uow:
        if not uow.productos.get_by_id(producto_id):
            raise AppError(404, "Producto no encontrado", "NOT_FOUND")
        if not uow.ingredientes.get_by_id(ingrediente_id):
            raise AppError(404, "Ingrediente no encontrado", "NOT_FOUND")
        uow.productos.asignar_ingrediente(producto_id, ingrediente_id)
    return {"detail": "Ingrediente asignado"}


@router.delete(
    "/{producto_id}/ingredientes/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def quitar_ingrediente(
    producto_id: int, ingrediente_id: int, _=Depends(require_role(["ADMIN"]))
):
    with UnitOfWork() as uow:
        uow.productos.quitar_ingrediente(producto_id, ingrediente_id)


ingredientes_router = APIRouter(prefix="/api/v1/ingredientes", tags=["ingredientes"])


@ingredientes_router.get("", response_model=list[IngredienteRead])
def list_ingredientes():
    with UnitOfWork() as uow:
        return uow.ingredientes.list_activos()


@ingredientes_router.post("", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def create_ingrediente(data: IngredienteCreate, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        if uow.ingredientes.get_by_nombre(data.nombre):
            raise AppError(400, "Ya existe ese ingrediente", "DUPLICATE_NAME", "nombre")
        from app.modules.productos.model import Ingrediente

        ingrediente = Ingrediente(nombre=data.nombre, es_alergeno=data.es_alergeno)
        return uow.ingredientes.create(ingrediente)


@ingredientes_router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingrediente(ingrediente_id: int, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente:
            raise AppError(404, "Ingrediente no encontrado", "NOT_FOUND")
        uow.ingredientes.soft_delete(ingrediente)
