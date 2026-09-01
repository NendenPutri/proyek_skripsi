from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.models.admin import Admin
from app.db.session import get_db
from app.repositories.admin_repository import get_admin_by_email, get_admin_by_id
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse, AdminResponse

bearer_scheme = HTTPBearer(auto_error=False)

INVALID_LOGIN_MESSAGE = "Email atau password tidak valid."


def authenticate_admin(db: Session, payload: AdminLoginRequest) -> AdminLoginResponse:
    """Validate admin credentials and return an access token."""
    admin = get_admin_by_email(db, payload.email)
    if not admin or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_LOGIN_MESSAGE,
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun admin tidak aktif.",
        )

    token = create_access_token(
        subject=str(admin.id),
        claims={"email": admin.email},
    )
    settings = get_settings()

    return AdminLoginResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
        admin=AdminResponse.model_validate(admin),
    )


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    """Return the active admin represented by a valid bearer token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token autentikasi wajib dikirim.",
        )

    try:
        payload = decode_access_token(credentials.credentials)
        admin_id = int(payload.get("sub", ""))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid.",
        ) from None

    admin = get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid.",
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun admin tidak aktif.",
        )

    return admin
