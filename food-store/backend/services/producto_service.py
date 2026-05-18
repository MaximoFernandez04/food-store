from fastapi import HTTPException, status
from datetime import datetime
from backend.models.producto import Producto
from backend.repositories.producto_repository import ProductoRepository

class ProductoService:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def create_producto(self, producto: Producto):
        if producto.precio <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0",
            )

        if producto.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser menor a 0",
            )

        existing_producto = self.producto_repository.get_by_nombre(producto.nombre)
        if existing_producto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un producto con ese nombre",
            )

        producto.fecha_actualizacion = datetime.utcnow()
        self.producto_repository.add(producto)

    def update_producto(self, producto: Producto, updates: dict):
        if "precio" in updates and updates["precio"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0",
            )

        if "stock" in updates and updates["stock"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser menor a 0",
            )

        for key, value in updates.items():
            setattr(producto, key, value)

        producto.fecha_actualizacion = datetime.utcnow()
        self.producto_repository.add(producto)

    def delete_producto(self, producto: Producto):
        self.producto_repository.delete(producto)