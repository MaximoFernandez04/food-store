from fastapi import APIRouter, Depends, status

from app.core.deps import require_role
from app.core.exceptions import AppError
from app.core.uow import UnitOfWork
from app.modules.categorias import service
from app.modules.categorias.schema import (
    CategoriaArbolNode,
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate,
)

router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaRead])
def list_categorias():
    with UnitOfWork() as uow:
        return uow.categorias.list_activas()


@router.get("/arbol", response_model=list[CategoriaArbolNode])
def arbol_categorias():
    with UnitOfWork() as uow:
        return uow.categorias.arbol_completo()


@router.get("/{categoria_id}", response_model=CategoriaRead)
def get_categoria(categoria_id: int):
    with UnitOfWork() as uow:
        categoria = uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise AppError(404, "Categoría no encontrada", "NOT_FOUND")
        return categoria


@router.post("", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def create_categoria(data: CategoriaCreate, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        return service.create_categoria(uow, data)


@router.put("/{categoria_id}", response_model=CategoriaRead)
def update_categoria(
    categoria_id: int, data: CategoriaUpdate, _=Depends(require_role(["ADMIN"]))
):
    with UnitOfWork() as uow:
        return service.update_categoria(uow, categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, _=Depends(require_role(["ADMIN"]))):
    with UnitOfWork() as uow:
        service.soft_delete_categoria(uow, categoria_id)
