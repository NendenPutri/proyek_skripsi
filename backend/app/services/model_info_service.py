import json
from functools import lru_cache
from typing import Any

from fastapi import HTTPException

from app.core.paths import MODEL_METADATA_PATH
from app.services.data_loader import get_dataset_status
from app.services.model_loader import get_model_status


@lru_cache(maxsize=1)
def load_model_metadata() -> dict[str, Any]:
    if not MODEL_METADATA_PATH.is_file():
        raise HTTPException(
            status_code=503,
            detail="Metadata model belum tersedia di models/model_metadata.json.",
        )

    try:
        with MODEL_METADATA_PATH.open(encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail="Metadata model bukan JSON yang valid.",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Metadata model tidak dapat dibaca.",
        ) from exc

    if not isinstance(metadata, dict):
        raise HTTPException(
            status_code=500,
            detail="Metadata model harus berupa object JSON.",
        )
    return metadata


def get_model_info() -> dict[str, Any]:
    """Return model metadata or a minimal status-based fallback."""
    if MODEL_METADATA_PATH.is_file():
        metadata = load_model_metadata()
        private_keys = {"feature_statistics", "training_rows", "internal_notes"}
        return {
            key: value for key, value in metadata.items() if key not in private_keys
        }

    dataset_status = get_dataset_status()
    model_status = get_model_status()
    return {
        "nama_proyek": "Sistem Rekomendasi Pemilihan Laptop",
        "algoritma": "Naive Bayes",
        "jenis_model": None,
        "tanggal_training": None,
        "dataset_final": dataset_status,
        "target": None,
        "fitur_model": [],
        "kelas": [
            "Administrasi/Perkantoran",
            "Programming",
            "Desain Grafis",
            "Editing Video",
        ],
        "metrics": None,
        "catatan": [
            "Metadata model belum tersedia.",
            model_status["message"],
            "Metrik evaluasi tidak ditampilkan tanpa model_metadata.json.",
        ],
    }
