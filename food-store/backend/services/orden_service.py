from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.models import Orden, ItemOrden, Producto
from backend.schemas import OrdenCreate
from datetime import datetime

def crear_orden(db: Session, data: OrdenCreate):
    try:
        # Crear la orden inicial
        nueva_orden = Orden(fecha=datetime.utcnow(), usuario_id=data.usuario_id)
        db.add(nueva_orden)
        db.flush()  # Necesario para obtener el ID de la orden antes de commit

        # Procesar cada item
        for item in data.items:
            # Buscar el producto
            producto = db.query(Producto).filter(Producto.id == item.producto_id).first()

            if not producto:
                raise ValueError(f"Producto con ID {item.producto_id} no existe.")

            # Verificar stock
            if producto.stock < item.cantidad:
                raise ValueError(f"Stock insuficiente para el producto {producto.nombre}.")

            # Descontar stock
            producto.stock -= item.cantidad

            # Crear el ItemOrden
            nuevo_item = ItemOrden(
                orden_id=nueva_orden.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio
            )
            db.add(nuevo_item)

        # Commit de la transacción si todo está bien
        db.commit()

        return nueva_orden

    except Exception as e:
        db.rollback()  # Revertir transacción en caso de error
        raise e