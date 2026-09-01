from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.services.health_service import get_health_status
from app.utils.response import success_response

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=ApiResponse[dict[str, object]])
async def health_check() -> dict[str, object]:
    """Return application and artifact availability status."""
    return success_response(
        "API berjalan.",
        get_health_status(),
    )
