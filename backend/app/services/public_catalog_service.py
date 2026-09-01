from decimal import Decimal
from typing import Any

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.laptop import Laptop
from app.repositories.laptop_repository import list_active_laptops_for_public
from app.services.data_loader import load_laptop_dataset

PUBLIC_CATALOG_COLUMNS = [
    "model",
    "brand_name",
    "price",
    "price_original",
    "price_currency",
    "price_idr",
    "rating",
    "processor",
    "processor_brand",
    "processor_series",
    "processor_score",
    "processor_level",
    "ram",
    "ram_num",
    "ram_class",
    "memory_type",
    "memory_size",
    "storage_class",
    "gpu_brand",
    "gpu_type",
    "gpu_score",
    "gpu_level",
    "os",
    "os_family",
    "display_size",
    "display_class",
    "resolution_height",
    "resolution_width",
    "resolution_class",
    "touch_screen",
    "touchscreen_label",
    "warranty",
    "warranty_class",
    "price_class",
    "label_kebutuhan",
    "predicted_label",
    "prediction_confidence",
    "alasan_label",
    "prob_administrasi_perkantoran",
    "prob_desain_grafis",
    "prob_editing_video",
    "prob_programming",
]


def _to_python(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "item"):
        return value.item()
    return value


def _clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    cleaned = dataframe.copy()
    cleaned = cleaned.astype(object).where(pd.notna(cleaned), None)
    return cleaned


def _dedupe_key(dataframe: pd.DataFrame) -> pd.Series:
    brand = dataframe.get("brand_name", pd.Series("", index=dataframe.index))
    model = dataframe.get("model", pd.Series("", index=dataframe.index))
    return (
        brand.fillna("").astype(str).str.strip().str.lower()
        + "::"
        + model.fillna("").astype(str).str.strip().str.lower()
    )


def _mysql_laptop_to_public_record(laptop: Laptop) -> dict[str, Any]:
    record = {column: _to_python(getattr(laptop, column, None)) for column in PUBLIC_CATALOG_COLUMNS}
    record["label_kebutuhan"] = laptop.predicted_category
    record["predicted_label"] = laptop.predicted_category
    record["prediction_confidence"] = _to_python(laptop.prediction_confidence)
    record["source"] = laptop.source
    record["_source_priority"] = 1
    return record


def load_active_mysql_laptops_as_dataframe(db: Session | None) -> pd.DataFrame:
    """Load active MySQL laptops as a public-catalog shaped DataFrame."""
    if db is None:
        return pd.DataFrame(columns=[*PUBLIC_CATALOG_COLUMNS, "source", "_source_priority"])

    rows = list_active_laptops_for_public(db)
    records = [_mysql_laptop_to_public_record(row) for row in rows]
    return pd.DataFrame(records, columns=[*PUBLIC_CATALOG_COLUMNS, "source", "_source_priority"])


def merge_csv_and_mysql_laptops(db: Session | None = None) -> pd.DataFrame:
    """Merge CSV rows with active MySQL rows.

    Dedupe rule: rows are considered the same laptop when normalized
    `brand_name + model` matches. CSV rows have priority 0, active MySQL rows have
    priority 1, so admin updates replace CSV rows for identical brand/model pairs.
    """
    csv_data = load_laptop_dataset().copy()
    for column in PUBLIC_CATALOG_COLUMNS:
        if column not in csv_data.columns:
            csv_data[column] = None
    csv_data = csv_data[PUBLIC_CATALOG_COLUMNS]
    csv_data["source"] = "csv"
    csv_data["_source_priority"] = 0

    try:
        mysql_data = load_active_mysql_laptops_as_dataframe(db)
    except SQLAlchemyError:
        mysql_data = pd.DataFrame(columns=[*PUBLIC_CATALOG_COLUMNS, "source", "_source_priority"])

    combined = pd.concat([csv_data, mysql_data], ignore_index=True)
    if combined.empty:
        return combined.drop(columns=["_source_priority"], errors="ignore")

    combined["_dedupe_key"] = _dedupe_key(combined)
    combined = combined.sort_values(
        by=["_dedupe_key", "_source_priority"],
        ascending=[True, True],
        kind="mergesort",
    )
    combined = combined.drop_duplicates(subset="_dedupe_key", keep="last")
    combined = combined.drop(columns=["_dedupe_key", "_source_priority"], errors="ignore")
    return _clean_dataframe(combined.reset_index(drop=True))
