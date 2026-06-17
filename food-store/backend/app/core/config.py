"""
Configuración centralizada de la aplicación.

Todo lo que en el repo anterior estaba hardcodeado (SECRET_KEY, DATABASE_URL
apuntando a sqlite, expiraciones de token) ahora se lee desde variables de
entorno, tal como exige la sección 10.1 de la especificación v5.0.

Nunca importes os.environ directamente en otro módulo: importá `settings`
desde aquí para tener una única fuente de verdad.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Base de datos
    database_url: str = "postgresql://user:password@localhost:5432/foodstore_db"

    # JWT
    secret_key: str = "CHANGE-ME-this-is-not-secure-min-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # MercadoPago
    mp_access_token: str = ""
    mp_public_key: str = ""
    mp_notification_url: str = ""

    # Rate limiting
    login_rate_limit: str = "5/15minutes"


settings = Settings()
