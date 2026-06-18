"""
Entry point. Este archivo no existía en el repo (por eso nada arrancaba).

uvicorn app.main:app --reload
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.exceptions import AppError
from app.core.rate_limit import limiter
from app.modules.auth.router import router as auth_router
from app.modules.categorias.router import router as categorias_router
from app.modules.direcciones.router import router as direcciones_router
from app.modules.pagos.router import router as pagos_router
from app.modules.pedidos.router import router as pedidos_router
from app.modules.productos.router import ingredientes_router, router as productos_router

# Importa todos los módulos con modelos SQLModel para que la metadata
# (usada por Alembic y por create_all en entornos de test) los conozca.
from app.modules.categorias import model as _categorias_model  # noqa: F401
from app.modules.direcciones import model as _direcciones_model  # noqa: F401
from app.modules.pagos import model as _pagos_model  # noqa: F401
from app.modules.pedidos import model as _pedidos_model  # noqa: F401
from app.modules.productos import model as _productos_model  # noqa: F401
from app.modules.refreshtokens import model as _refreshtokens_model  # noqa: F401
from app.modules.usuarios import model as _usuarios_model  # noqa: F401

app = FastAPI(title="Food Store API", version="5.0.0")

app.state.limiter = limiter
app.add_middleware(CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Demasiados intentos, intentá más tarde", "code": "RATE_LIMITED"},
        headers={"Retry-After": "900"},
    )


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code, "field": exc.field},
    )


app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(productos_router)
app.include_router(ingredientes_router)
app.include_router(direcciones_router)
app.include_router(pedidos_router)
app.include_router(pagos_router)


@app.get("/health")
def health():
    return {"status": "ok"}
