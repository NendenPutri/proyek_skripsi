from functools import lru_cache
from typing import Any

import pandas as pd
from fastapi import HTTPException

from app.core.paths import DATASET_PATH

REQUIRED_DATASET_COLUMNS = {
    "model",
    "brand_name",
    "price",
    "rating",
    "processor_series",
    "processor_level",
    "ram_num",
    "memory_size",
    "memory_type",
    "gpu_type",
    "gpu_level",
    "os_family",
    "label_kebutuhan",
}


def dataset_exists() -> bool:
    return DATASET_PATH.is_file()


@lru_cache(maxsize=1)
def load_laptop_dataset() -> pd.DataFrame:
    if not dataset_exists():
        raise HTTPException(
            status_code=503,
            detail="Dataset laptop belum tersedia di data/laptops_backend_ready.csv.",
        )

    try:
        dataset = pd.read_csv(DATASET_PATH)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Dataset laptop tidak dapat dibaca sebagai CSV.",
        ) from exc

    if dataset.empty:
        raise HTTPException(
            status_code=500,
            detail="Dataset laptop tersedia tetapi tidak memiliki data.",
        )

    missing_columns = sorted(REQUIRED_DATASET_COLUMNS - set(dataset.columns))
    if missing_columns:
        raise HTTPException(
            status_code=500,
            detail=(
                "Dataset laptop belum memiliki kolom wajib: "
                + ", ".join(missing_columns)
                + "."
            ),
        )
    return dataset


def get_dataset_status() -> dict[str, Any]:
    if not dataset_exists():
        return {
            "exists": False,
            "ready": False,
            "path": "data/laptops_backend_ready.csv",
            "message": "Dataset laptop belum tersedia.",
        }

    try:
        dataset = load_laptop_dataset()
    except HTTPException as exc:
        return {
            "exists": True,
            "ready": False,
            "path": "data/laptops_backend_ready.csv",
            "message": str(exc.detail),
        }

    return {
        "exists": True,
        "ready": True,
        "path": "data/laptops_backend_ready.csv",
        "rows": int(len(dataset)),
        "columns": int(len(dataset.columns)),
        "message": "Dataset laptop siap digunakan.",
    }
