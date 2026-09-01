from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.admin import Admin
from app.db.session import get_db
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse, AdminResponse
from app.schemas.common import ApiResponse
from app.services.auth_service import authenticate_admin, get_current_admin
from app.utils.response import success_response

router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


@router.post("/login", response_model=ApiResponse[AdminLoginResponse])
async def login_admin(
    payload: AdminLoginRequest,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Authenticate an active admin and issue a JWT access token."""
    result = authenticate_admin(db, payload)
    return success_response("Login admin berhasil.", result.model_dump())


@router.get("/me", response_model=ApiResponse[AdminResponse])
async def get_me(
    current_admin: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Return the authenticated active admin profile."""
    admin = AdminResponse.model_validate(current_admin)
    return success_response("Data admin berhasil diambil.", admin.model_dump())
