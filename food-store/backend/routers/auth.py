from fastapi import APIRouter, Depends, HTTPException, status
from backend.auth.dependencies import get_current_user
from backend.auth.jwt_handler import create_access_token
from backend.auth.security import hash_password, verify_password
from backend.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from backend.models.usuario import Usuario
from backend.repositories.usuario_repository import UsuarioRepository
from backend.core.database import SessionManager

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register_user(
    user_data: RegisterRequest,
    db = Depends(SessionManager())):
    user_repo = UsuarioRepository(db)

    # Check if email is already taken
    if user_repo.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = Usuario(
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role
    )
    user_repo.add(new_user)
    db.commit()

    # Generate token
    token = create_access_token({"sub": new_user.id})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login_user(
    login_data: LoginRequest,
    db = Depends(SessionManager())):
    user_repo = UsuarioRepository(db)
    user = user_repo.get_by_email(login_data.email)

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate token
    token = create_access_token({"sub": user.id})
    return TokenResponse(access_token=token)

@router.get("/me")
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    return current_user