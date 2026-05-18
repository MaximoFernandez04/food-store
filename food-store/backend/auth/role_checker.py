from fastapi import Depends, HTTPException, status
from backend.auth.dependencies import get_current_user
from backend.models.usuario import Usuario

def verify_role(required_roles: list[str]):
    def role_verification(user: Usuario = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions, requires one of: {', '.join(required_roles)}",
            )
        return user
    return role_verification