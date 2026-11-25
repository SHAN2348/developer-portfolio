
from fastapi import APIRouter, HTTPException, status

from app.schemas.admin import AdminLogin, TokenResponse
from app.services import admin_service
from app.core.password import verify_password
from app.core.token import create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse)
async def admin_login(credentials: AdminLogin):
    admin = await admin_service.get_admin_by_username(
        credentials.username
    )

    if not admin or not verify_password(
        credentials.password,
        admin["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        str(admin["_id"])
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
