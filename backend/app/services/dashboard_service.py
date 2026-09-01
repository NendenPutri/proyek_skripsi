from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from app.schemas.dashboard import (
    AdminDashboardStats,
    CategoryDistributionItem,
)
from app.services.public_catalog_service import merge_csv_and_mysql_laptops

NEED_LABELS = [
    "Administrasi/Perkantoran",
    "Programming",
    "Desain Grafis",
    "Editing Video",
]

def _clean_value(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _category_series(dataset: pd.DataFrame) -> pd.Series:
    if dataset.empty:
        return pd.Series(dtype=str)

    label = dataset.get("label_kebutuhan", pd.Series("", index=dataset.index))
    predicted = dataset.get("predicted_label", pd.Series("", index=dataset.index))
    return label.where(label.notna() & (label.astype(str).str.strip() != ""), predicted)


def _build_category_distribution(dataset: pd.DataFrame) -> list[CategoryDistributionItem]:
    categories = _category_series(dataset).map(_clean_value)
    counts = categories.value_counts().to_dict()

    return [
        CategoryDistributionItem(category=category, count=int(counts.get(category, 0)))
        for category in NEED_LABELS
    ]


def get_admin_dashboard_stats(db: Session) -> AdminDashboardStats:
    """Return dashboard statistics from the deduped public catalog."""
    dataset = merge_csv_and_mysql_laptops(db)

    return AdminDashboardStats(
        category_distribution=_build_category_distribution(dataset),
    )
