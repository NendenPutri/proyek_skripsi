from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ModelInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nama_proyek: str | None = None
    algoritma: str | None = None
    jenis_model: str | None = None
    tanggal_training: str | None = None
    dataset_final: dict[str, Any] | None = None
    target: str | None = None
    fitur_model: list[str] = Field(default_factory=list)
    kelas: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] | None = None
    catatan: list[str] = Field(default_factory=list)
