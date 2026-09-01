from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AdminLaptopInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    model: str = Field(min_length=1, max_length=255)
    brand_name: str = Field(min_length=1, max_length=100)
    price: float | None = Field(default=None, ge=0)
    price_original: float | None = Field(default=None, ge=0)
    price_currency: str | None = Field(default=None, max_length=10)
    price_idr: float | None = Field(default=None, ge=0)
    rating: float | None = Field(default=None, ge=0, le=5)
    processor: str | None = Field(default=None, max_length=255)
    processor_brand: str = Field(min_length=1, max_length=100)
    processor_series: str = Field(min_length=1, max_length=100)
    processor_score: float | None = Field(default=None, ge=0)
    processor_level: str = Field(min_length=1, max_length=50)
    ram: str | None = Field(default=None, max_length=100)
    ram_num: int | None = Field(default=None, ge=0)
    ram_class: str = Field(min_length=1, max_length=50)
    memory_type: str = Field(min_length=1, max_length=50)
    memory_size: int | None = Field(default=None, ge=0)
    storage_class: str = Field(min_length=1, max_length=50)
    gpu_brand: str = Field(min_length=1, max_length=100)
    gpu_type: str = Field(min_length=1, max_length=50)
    gpu_score: float | None = Field(default=None, ge=0)
    gpu_level: str = Field(min_length=1, max_length=100)
    os: str | None = Field(default=None, max_length=100)
    os_family: str = Field(min_length=1, max_length=50)
    display_size: float | None = Field(default=None, ge=0)
    display_class: str = Field(min_length=1, max_length=50)
    resolution_height: int | None = Field(default=None, ge=0)
    resolution_width: int | None = Field(default=None, ge=0)
    resolution_class: str = Field(min_length=1, max_length=50)
    touch_screen: bool | None = None
    touchscreen_label: str = Field(min_length=1, max_length=20)
    warranty: int | None = Field(default=None, ge=0)
    warranty_class: str = Field(min_length=1, max_length=50)
    price_class: str = Field(min_length=1, max_length=50)

    @field_validator("touch_screen", mode="before")
    @classmethod
    def normalize_touch_screen(cls, value: Any) -> bool | None:
        if hasattr(value, "item"):
            value = value.item()
        if value is None or isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "yes", "1"}:
                return True
            if normalized in {"false", "no", "0"}:
                return False
        raise ValueError("touch_screen harus bernilai boolean, Yes, atau No.")


class AdminLaptopInferenceResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    catalog: dict[str, Any]
    model_features: dict[str, str]
    predicted_label: str
    prediction_confidence: float | None = None
    class_probabilities: dict[str, float] | None = None


class AdminLaptopResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    brand_name: str
    price: float | None = None
    price_original: float | None = None
    price_currency: str | None = None
    price_idr: float | None = None
    rating: float | None = None
    processor: str | None = None
    processor_brand: str | None = None
    processor_series: str | None = None
    processor_score: float | None = None
    processor_level: str | None = None
    ram: str | None = None
    ram_num: int | None = None
    ram_class: str | None = None
    memory_type: str | None = None
    memory_size: int | None = None
    storage_class: str | None = None
    gpu_brand: str | None = None
    gpu_type: str | None = None
    gpu_score: float | None = None
    gpu_level: str | None = None
    os: str | None = None
    os_family: str | None = None
    display_size: float | None = None
    display_class: str | None = None
    resolution_height: int | None = None
    resolution_width: int | None = None
    resolution_class: str | None = None
    touch_screen: bool | None = None
    touchscreen_label: str | None = None
    warranty: int | None = None
    warranty_class: str | None = None
    price_class: str | None = None
    predicted_category: str | None = None
    prediction_confidence: float | None = None
    source: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminLaptopPagination(BaseModel):
    page: int = Field(ge=1)
    limit: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class AdminLaptopListResponse(BaseModel):
    items: list[AdminLaptopResponse]
    pagination: AdminLaptopPagination


class AdminLaptopSort(str):
    pass


AdminLaptopStatusFilter = Literal["all", "active", "inactive"]
