from functools import lru_cache
from typing import Any

from fastapi import HTTPException
import joblib

from app.core.paths import MODEL_PATH


def model_exists() -> bool:
    return MODEL_PATH.is_file()


@lru_cache(maxsize=1)
def load_model() -> Any:
    if not model_exists():
        raise HTTPException(
            status_code=503,
            detail=(
                "Model belum tersedia di "
                "models/naive_bayes_laptop_pipeline.joblib."
            ),
        )

    try:
        return joblib.load(MODEL_PATH)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Model joblib tidak dapat dimuat.",
        ) from exc


def get_model_status() -> dict[str, Any]:
    if not model_exists():
        return {
            "exists": False,
            "ready": False,
            "path": "models/naive_bayes_laptop_pipeline.joblib",
            "message": "Model Naive Bayes belum tersedia.",
        }

    try:
        load_model()
    except HTTPException as exc:
        return {
            "exists": True,
            "ready": False,
            "path": "models/naive_bayes_laptop_pipeline.joblib",
            "message": str(exc.detail),
        }

    return {
        "exists": True,
        "ready": True,
        "path": "models/naive_bayes_laptop_pipeline.joblib",
        "message": "Model Naive Bayes siap digunakan.",
    }


def load_naive_bayes_model() -> Any:
    return load_model()
