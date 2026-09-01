from pydantic import BaseModel, ConfigDict, Field


class Laptop(BaseModel):
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
    label_kebutuhan: str | None = None
    predicted_label: str | None = None
    prediction_confidence: float | None = None
    alasan_label: str | None = None


class LaptopListData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[Laptop] = Field(default_factory=list)
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
