"""
Seguridad: hashing de contraseñas (bcrypt, cost>=12) y JWT.

A diferencia del código viejo, SECRET_KEY sale de settings (env), el access
token dura lo que dice la spec (30 min) y agregamos generación/verificación
del refresh token (que el código viejo no tenía: no existía /auth/refresh
ni /auth/logout reales).
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(usuario_id: int, roles: list[str]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(usuario_id), "roles": roles, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
    except JWTError as exc:
        raise ValueError("Token inválido o expirado") from exc
    if payload.get("type") != "access":
        raise ValueError("Tipo de token incorrecto")
    return payload


def generate_refresh_token() -> tuple[str, str, datetime]:
    """Devuelve (token_plano, token_hash, expires_at).

    El token plano es lo único que se le entrega al cliente; en la base
    sólo se persiste el hash (token_hash), tal como exige la spec.
    """
    raw_token = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    return raw_token, token_hash, expires_at


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()
