from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.admin import Admin
from app.db.session import get_db
from app.schemas.common import ApiResponse
from app.schemas.dashboard import AdminDashboardStats
from app.services.auth_service import get_current_admin
from app.services.dashboard_service import get_admin_dashboard_stats
from app.utils.response import success_response

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/stats", response_model=ApiResponse[AdminDashboardStats])
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Return admin dashboard statistics from real catalog data."""
    result = get_admin_dashboard_stats(db)
    return success_response(
        "Statistik dashboard berhasil diambil",
        result.model_dump(),
    )
