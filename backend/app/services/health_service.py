from typing import Any

from app.core.config import get_settings
from app.core.paths import FRONTEND_OPTIONS_PATH, MODEL_METADATA_PATH
from app.db.health import check_database_connection
from app.services.data_loader import dataset_exists
from app.services.model_loader import model_exists


def get_health_status() -> dict[str, Any]:
    """Return public health status without changing legacy response fields."""
    settings = get_settings()
    database_status = check_database_connection()
    dataset_available = dataset_exists()
    model_available = model_exists()
    options_available = FRONTEND_OPTIONS_PATH.is_file()
    metadata_available = MODEL_METADATA_PATH.is_file()
    database_available = bool(database_status["available"])
    is_ready = (
        dataset_available
        and model_available
        and options_available
        and metadata_available
        and database_available
    )

    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "dataset_available": dataset_available,
        "model_available": model_available,
        "options_available": options_available,
        "metadata_available": metadata_available,
        "database_available": database_available,
        "database": database_status,
        "status": "ready" if is_ready else "degraded",
    }
