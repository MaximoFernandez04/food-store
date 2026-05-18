from datetime import datetime
from pydantic import BaseModel

class OrdenResponse(BaseModel):
    id: int
    fecha: datetime
    estado: str
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True