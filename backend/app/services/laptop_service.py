from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from app.services.public_catalog_service import merge_csv_and_mysql_laptops
from app.services.scoring_service import calculate_price_score, calculate_rating_score

LAPTOP_LIST_COLUMNS = [
    "model",
    "brand_name",
    "price",
    "price_original",
    "price_currency",
    "price_idr",
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
    "predicted_label",
    "prediction_confidence",
    "alasan_label",
]


def dataframe_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a DataFrame into JSON-safe records."""
    serializable = dataframe.astype(object).where(pd.notna(dataframe), None)
    return serializable.to_dict(orient="records")


def filter_laptops(
    dataframe: pd.DataFrame, filters: dict[str, Any]
) -> pd.DataFrame:
    """Apply exact-match filters to a laptop DataFrame."""
    filtered = dataframe
    for column, value in filters.items():
        if column not in filtered.columns:
            raise ValueError(f"Filter '{column}' tidak tersedia pada dataset.")
        filtered = filtered[filtered[column] == value]
    return filtered


def _filter_by_brand(dataset: pd.DataFrame, brand: str | None) -> pd.DataFrame:
    if not brand or "brand_name" not in dataset.columns:
        return dataset

    return dataset[dataset["brand_name"].astype(str).str.lower() == brand.lower()]


def _filter_by_kebutuhan(dataset: pd.DataFrame, kebutuhan: str | None) -> pd.DataFrame:
    if not kebutuhan:
        return dataset

    matches = pd.Series(False, index=dataset.index)
    if "label_kebutuhan" in dataset.columns:
        matches = matches | (dataset["label_kebutuhan"] == kebutuhan)
    if "predicted_label" in dataset.columns:
        matches = matches | (dataset["predicted_label"] == kebutuhan)
    return dataset[matches]


def _filter_by_search(dataset: pd.DataFrame, search: str | None) -> pd.DataFrame:
    if not search:
        return dataset

    keyword = search.lower()
    matches = pd.Series(False, index=dataset.index)
    if "model" in dataset.columns:
        matches = matches | dataset["model"].fillna("").astype(str).str.lower().str.contains(
            keyword,
            regex=False,
        )
    if "brand_name" in dataset.columns:
        matches = matches | dataset["brand_name"].fillna("").astype(str).str.lower().str.contains(
            keyword,
            regex=False,
        )
    return dataset[matches]


def _numeric_series(dataset: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in dataset.columns:
        return pd.Series(default, index=dataset.index, dtype=float)

    return pd.to_numeric(dataset[column], errors="coerce").fillna(default)


def _price_column(dataset: pd.DataFrame) -> str:
    if "price_idr" in dataset.columns:
        return "price_idr"
    return "price"


def _kebutuhan_probability_column(kebutuhan: str | None) -> str | None:
    probability_columns = {
        "Administrasi/Perkantoran": "prob_administrasi_perkantoran",
        "Programming": "prob_programming",
        "Desain Grafis": "prob_desain_grafis",
        "Editing Video": "prob_editing_video",
    }
    return probability_columns.get(kebutuhan or "")


def _rank_laptops(dataset: pd.DataFrame, kebutuhan: str | None) -> pd.DataFrame:
    """Rank catalog rows so filtered pages do not depend on CSV order."""
    if dataset.empty:
        return dataset

    ranked = dataset.copy()

    exact_label = pd.Series(False, index=ranked.index)
    if kebutuhan:
        if "label_kebutuhan" in ranked.columns:
            exact_label = exact_label | (ranked["label_kebutuhan"] == kebutuhan)
        if "predicted_label" in ranked.columns:
            exact_label = exact_label | (ranked["predicted_label"] == kebutuhan)

    probability_column = _kebutuhan_probability_column(kebutuhan)
    if probability_column and probability_column in ranked.columns:
        confidence = _numeric_series(ranked, probability_column)
    else:
        confidence = _numeric_series(ranked, "prediction_confidence")

    rating_score = calculate_rating_score(
        ranked.get("rating", pd.Series(index=ranked.index))
    )
    price_score = calculate_price_score(
        ranked.get(_price_column(ranked), pd.Series(index=ranked.index))
    )

    ranked["_catalog_exact_score"] = exact_label.astype(int)
    ranked["_catalog_rank_score"] = (
        (confidence.clip(lower=0.0, upper=1.0) * 0.5)
        + (rating_score * 0.25)
        + (price_score * 0.25)
    ).fillna(0.0)

    ranked = ranked.sort_values(
        by=["_catalog_exact_score", "_catalog_rank_score", _price_column(ranked)],
        ascending=[False, False, True],
        kind="mergesort",
    )
    return ranked.drop(columns=["_catalog_exact_score", "_catalog_rank_score"])


def get_laptops(
    limit: int = 20,
    brand: str | None = None,
    kebutuhan: str | None = None,
    search: str | None = None,
    db: Session | None = None,
) -> dict[str, Any]:
    """Load public laptops from CSV plus active MySQL rows and apply filters."""
    dataset = merge_csv_and_mysql_laptops(db)
    filtered = _filter_by_brand(dataset, brand)
    filtered = _filter_by_kebutuhan(filtered, kebutuhan)
    filtered = _filter_by_search(filtered, search)
    filtered = _rank_laptops(filtered, kebutuhan)

    visible_columns = [column for column in LAPTOP_LIST_COLUMNS if column in filtered.columns]
    if visible_columns:
        filtered = filtered[visible_columns]

    items = dataframe_to_records(filtered.head(limit))
    return {
        "items": items,
        "total": len(filtered),
        "limit": limit,
        "offset": 0,
    }
