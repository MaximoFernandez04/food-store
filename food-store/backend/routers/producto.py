from fastapi import APIRouter, Depends, HTTPException, status
from backend.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from backend.models.producto import Producto
from backend.repositories.producto_repository import ProductoRepository
from backend.services.producto_service import ProductoService
from backend.core.unit_of_work import UnitOfWork
from backend.auth.dependencies import get_current_user
from backend.auth.role_checker import verify_role
from typing import List

router = APIRouter()

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(
    producto_data: ProductoCreate,
    uow: UnitOfWork = Depends(),
    user = Depends(verify_role(["ADMIN", "GESTOR_STOCK"]))
):
    service = ProductoService(uow.producto_repository)
    new_producto = Producto(**producto_data.dict())
    service.create_producto(new_producto)
    uow.commit()
    return new_producto

@router.get("/productos", response_model=List[ProductoResponse])
def list_productos(uow: UnitOfWork = Depends()):
    repository = uow.producto_repository
    return repository.list()

@router.get("/productos/{id}", response_model=ProductoResponse)
def get_producto(id: int, uow: UnitOfWork = Depends()):
    repository = uow.producto_repository
    producto = repository.get_by_id(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado",
        )
    return producto

@router.patch("/productos/{id}", response_model=ProductoResponse)
def update_producto(
    id: int,
    producto_data: ProductoUpdate,
    uow: UnitOfWork = Depends(),
    user = Depends(verify_role(["ADMIN", "GESTOR_STOCK"]))
):
    service = ProductoService(uow.producto_repository)
    producto = uow.producto_repository.get_by_id(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado",
        )
    service.update_producto(producto, producto_data.dict(exclude_unset=True))
    uow.commit()
    return producto

@router.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    id: int,
    uow: UnitOfWork = Depends(),
    user = Depends(verify_role(["ADMIN", "GESTOR_STOCK"]))
):
    service = ProductoService(uow.producto_repository)
    producto = uow.producto_repository.get_by_id(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado",
        )
    service.delete_producto(producto)
    uow.commit()