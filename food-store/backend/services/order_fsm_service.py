from datetime import datetime
from backend.models.orden import Orden
from fastapi import HTTPException, status
from backend.repositories.orden_repository import OrdenRepository

class OrderFsmService:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    # Estados válidos y transiciones
    state_transitions = {
        "PENDIENTE": ["PAGADO", "CANCELADO"],
        "PAGADO": ["PREPARANDO"],
        "PREPARANDO": ["ENVIADO"],
        "ENVIADO": ["ENTREGADO"],
    }

    def validate_transition(self, current_state: str, new_state: str):
        if current_state == new_state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estado ya es {current_state}",
            )

        if new_state not in self.state_transitions.get(current_state, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transición inválida: {current_state} -> {new_state}",
            )

    def update_state(self, orden: Orden, new_state: str):
        self.validate_transition(orden.estado, new_state)

        # Actualizar orden
        orden.estado = new_state
        orden.fecha_actualizacion = datetime.utcnow()
        self.orden_repository.add(orden)

        return orden