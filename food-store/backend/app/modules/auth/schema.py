from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    apellido: str = Field(min_length=2, max_length=80)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=30)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    roles: list[str]
    created_at: datetime

    class Config:
        from_attributes = True
