from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Laptop(Base):
    """Laptop data added through admin input and predicted by the model."""

    __tablename__ = "laptops"
    __table_args__ = (
        UniqueConstraint(
            "brand_name",
            "model",
            "source",
            name="uq_laptops_brand_model_source",
        ),
        Index("ix_laptops_brand_name", "brand_name"),
        Index("ix_laptops_model", "model"),
        Index("ix_laptops_predicted_category", "predicted_category"),
        Index("ix_laptops_is_active", "is_active"),
        Index("ix_laptops_source", "source"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Catalog fields and normalized columns aligned with the prepared CSV.
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    brand_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    price_original: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    price_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    price_idr: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    processor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    processor_brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    processor_series: Mapped[str | None] = mapped_column(String(100), nullable=True)
    processor_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    processor_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ram: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ram_num: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ram_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    memory_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    memory_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    storage_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gpu_brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gpu_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gpu_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    gpu_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    os: Mapped[str | None] = mapped_column(String(100), nullable=True)
    os_family: Mapped[str | None] = mapped_column(String(50), nullable=True)
    display_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    display_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resolution_height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resolution_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resolution_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    touch_screen: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    touchscreen_label: Mapped[str | None] = mapped_column(String(20), nullable=True)
    warranty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    warranty_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    price_class: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Prediction fields for admin-created laptop rows.
    predicted_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prediction_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    alasan_label: Mapped[str | None] = mapped_column(Text, nullable=True)
    prob_administrasi_perkantoran: Mapped[float | None] = mapped_column(Float, nullable=True)
    prob_desain_grafis: Mapped[float | None] = mapped_column(Float, nullable=True)
    prob_editing_video: Mapped[float | None] = mapped_column(Float, nullable=True)
    prob_programming: Mapped[float | None] = mapped_column(Float, nullable=True)

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default="admin",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="1",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
