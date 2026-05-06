from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas import OrdenCreate, OrdenResponse
from backend.services.orden_service import crear_orden
from backend.database import get_db

router = APIRouter()

@router.post("/ordenes", response_model=OrdenResponse)
def create_orden(orden_data: OrdenCreate, db: Session = Depends(get_db)):
    try:
        nueva_orden = crear_orden(db, orden_data)
        return nueva_orden
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al procesar la orden.")