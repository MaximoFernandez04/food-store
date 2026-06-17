"""
Errores estándar RFC 7807 (sección 5 de la spec):
{ "detail": "mensaje", "code": "ERROR_CODE", "field": "campo_opcional" }
"""
from typing import Optional

from fastapi import HTTPException


class AppError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str,
        field: Optional[str] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code
        self.field = field
