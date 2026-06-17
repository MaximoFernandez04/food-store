"""
Dominio 1 — Identidad (parte 1): Rol, Usuario, UsuarioRol.

Mapea la sección 3.1 de la especificación v5.0. RefreshToken vive en su
propio módulo (app/modules/refreshtokens) porque la spec lo define como
módulo separado en la tabla de "Módulos Backend (Feature-First)".
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Rol(SQLModel, table=True):
    __tablename__ = "rol"

    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: Optional[str] = None


class UsuarioRol(SQLModel, table=True):
    __tablename__ = "usuario_rol"

    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    rol_codigo: str = Field(foreign_key="rol.codigo", primary_key=True)
    asignado_por_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=80)
    apellido: str = Field(max_length=80)
    email: str = Field(max_length=254, index=True, unique=True)
    telefono: Optional[str] = Field(default=None, max_length=30)
    password_hash: str = Field(max_length=60)
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    refresh_tokens: list["RefreshToken"] = Relationship(  # noqa: F821
        back_populates="usuario"
    )
