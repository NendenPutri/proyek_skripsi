from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.services.options_service import get_options as get_options_service
from app.utils.response import success_response

router = APIRouter(tags=["Options"])


@router.get("/options", response_model=ApiResponse[object])
async def get_options() -> dict[str, object]:
    """Return dropdown options for the React frontend."""
    options = get_options_service()
    return success_response("Pilihan frontend berhasil dimuat.", options)
