from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.model_info import ModelInfo
from app.services.model_info_service import get_model_info
from app.utils.response import success_response

router = APIRouter(tags=["Model"])


@router.get("/model-info", response_model=ApiResponse[ModelInfo])
async def model_info() -> dict[str, object]:
    """Return safe model metadata for the frontend."""
    metadata = get_model_info()
    return success_response("Informasi model berhasil dimuat.", metadata)
