from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

KebutuhanLabel = Literal[
    "Administrasi/Perkantoran",
    "Programming",
    "Desain Grafis",
    "Editing Video",
]


class RecommendationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    kebutuhan: KebutuhanLabel
    budget_maksimal: float | None = Field(default=None, gt=0)
    ram_min: int | None = Field(default=None, gt=0)
    storage_min: int | None = Field(default=None, gt=0)
    brand: str | None = "Semua"
    os_family: str | None = "Semua"
    processor_min_level: str | None = "Semua"
    gpu_type: str | None = "Tidak wajib"
    touch_screen: str | None = "Semua"
    jumlah_hasil: int = Field(default=5, ge=1, le=50)


class RecommendationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: str | None = None
    brand_name: str | None = None
    price: float | None = None
    price_original: float | None = None
    price_currency: str | None = None
    price_idr: float | None = None
    rating: float | None = None
    processor_series: str | None = None
    processor_level: str | None = None
    ram_num: int | None = None
    memory_size: int | None = None
    memory_type: str | None = None
    gpu_type: str | None = None
    gpu_level: str | None = None
    os_family: str | None = None
    backend_predicted_label: str | None = None
    backend_confidence: float | None = None
    final_score: float | None = None
    alasan_rekomendasi: str | None = None
    unmet_filters: list[str] = Field(default_factory=list)
    match_percentage: float | None = None
    is_exact_match: bool = False


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    total: int = Field(ge=0)
    is_alternative: bool = False
    recommendations: list[RecommendationItem] = Field(default_factory=list)


# Dipertahankan sementara agar route yang ada tetap dapat diimpor.
RecommendationResult = RecommendationResponse
