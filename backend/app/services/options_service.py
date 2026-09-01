import json
from functools import lru_cache
from typing import Any

import pandas as pd
from fastapi import HTTPException

from app.core.paths import FRONTEND_OPTIONS_PATH
from app.services.data_loader import dataset_exists, load_laptop_dataset

NEED_LABELS = [
    "Administrasi/Perkantoran",
    "Programming",
    "Desain Grafis",
    "Editing Video",
]

REQUIRED_OPTIONS_KEYS = {
    "kebutuhan",
    "brand",
    "processor_brand",
    "processor_series",
    "processor_level",
    "ram_class",
    "memory_type",
    "storage_class",
    "gpu_brand",
    "ram_min",
    "storage_min",
    "gpu_type",
    "gpu_level",
    "os_family",
    "display_class",
    "resolution_class",
    "touch_screen",
    "warranty_class",
    "jumlah_hasil",
    "price_class",
    "price_min",
    "price_max",
    "price_note",
}


def _clean_string_options(dataset: pd.DataFrame, column: str) -> list[str]:
    if column not in dataset.columns:
        return []

    values = dataset[column].dropna().astype(str).str.strip()
    return sorted(value for value in values.unique().tolist() if value)


def _clean_numeric_options(dataset: pd.DataFrame, column: str) -> list[int]:
    if column not in dataset.columns:
        return []

    values = pd.to_numeric(dataset[column], errors="coerce").dropna().astype(int)
    return sorted(values.unique().tolist())


def _numeric_min_max(dataset: pd.DataFrame, column: str) -> tuple[float | None, float | None]:
    if column not in dataset.columns:
        return None, None

    values = pd.to_numeric(dataset[column], errors="coerce").dropna()
    if values.empty:
        return None, None
    return float(values.min()), float(values.max())


def _with_all_option(options: list[str]) -> list[str]:
    return ["Semua", *[option for option in options if option != "Semua"]]


def _with_not_required_option(options: list[str]) -> list[str]:
    return ["Tidak wajib", *[option for option in options if option != "Tidak wajib"]]


@lru_cache(maxsize=1)
def load_frontend_options() -> dict[str, Any]:
    if not FRONTEND_OPTIONS_PATH.is_file():
        raise HTTPException(
            status_code=503,
            detail="Pilihan frontend belum tersedia di data/frontend_options.json.",
        )

    try:
        with FRONTEND_OPTIONS_PATH.open(encoding="utf-8") as options_file:
            options = json.load(options_file)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail="File pilihan frontend bukan JSON yang valid.",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="File pilihan frontend tidak dapat dibaca.",
        ) from exc

    if not isinstance(options, dict):
        raise HTTPException(
            status_code=500,
            detail="File pilihan frontend harus berupa object JSON.",
        )

    missing_keys = sorted(REQUIRED_OPTIONS_KEYS - set(options))
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=(
                "File pilihan frontend belum memiliki key wajib: "
                + ", ".join(missing_keys)
                + "."
            ),
        )
    return options


def build_options_from_dataset() -> dict[str, Any]:
    """Build frontend dropdown options from the prepared laptop dataset."""
    dataset = load_laptop_dataset()
    price_min, price_max = _numeric_min_max(dataset, "price")

    return {
        "kebutuhan": NEED_LABELS,
        "brand": _with_all_option(_clean_string_options(dataset, "brand_name")),
        "processor_brand": _clean_string_options(dataset, "processor_brand"),
        "processor_series": _with_all_option(
            _clean_string_options(dataset, "processor_series")
        ),
        "processor_level": _with_all_option(
            _clean_string_options(dataset, "processor_level")
        ),
        "ram_class": _clean_string_options(dataset, "ram_class"),
        "memory_type": _clean_string_options(dataset, "memory_type"),
        "storage_class": _clean_string_options(dataset, "storage_class"),
        "ram_min": _clean_numeric_options(dataset, "ram_num"),
        "storage_min": _clean_numeric_options(dataset, "memory_size"),
        "gpu_brand": _clean_string_options(dataset, "gpu_brand"),
        "gpu_type": _with_not_required_option(_clean_string_options(dataset, "gpu_type")),
        "gpu_level": _with_all_option(_clean_string_options(dataset, "gpu_level")),
        "os_family": _with_all_option(_clean_string_options(dataset, "os_family")),
        "display_class": _clean_string_options(dataset, "display_class"),
        "resolution_class": _clean_string_options(dataset, "resolution_class"),
        "touch_screen": _with_all_option(_clean_string_options(dataset, "touch_screen")),
        "warranty_class": _clean_string_options(dataset, "warranty_class"),
        "jumlah_hasil": [5, 10, 15, 20, 50],
        "price_class": _clean_string_options(dataset, "price_class"),
        "price_min": price_min,
        "price_max": price_max,
        "price_note": "Satuan harga mengikuti dataset asli.",
    }


def get_options() -> dict[str, Any]:
    """Return frontend options from JSON, or derive them from the dataset."""
    if FRONTEND_OPTIONS_PATH.is_file():
        return load_frontend_options()

    if dataset_exists():
        return build_options_from_dataset()

    raise HTTPException(
        status_code=503,
        detail=(
            "Pilihan frontend belum tersedia dan dataset belum tersedia untuk "
            "membangun options."
        ),
    )


def get_frontend_options() -> dict[str, Any]:
    return get_options()
