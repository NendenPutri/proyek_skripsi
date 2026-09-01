from typing import Any

import pandas as pd

PROCESSOR_LEVEL_SCORES = {
    "Entry": 1,
    "Basic": 2,
    "Mid": 3,
    "High": 4,
    "Premium": 5,
}


def safe_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default

    try:
        number = float(value)
    except (TypeError, ValueError):
        return default

    if pd.isna(number):
        return default
    return number


def get_processor_level_score(level: Any) -> int:
    if level is None or pd.isna(level):
        return 0
    return PROCESSOR_LEVEL_SCORES.get(str(level).strip(), 0)


def calculate_price_score(series: pd.Series) -> pd.Series:
    prices = pd.to_numeric(series, errors="coerce")
    valid_prices = prices.dropna()

    if valid_prices.empty:
        return pd.Series(0.0, index=series.index)

    lowest = float(valid_prices.min())
    highest = float(valid_prices.max())
    if lowest == highest:
        return prices.notna().astype(float)

    scores = 1 - ((prices - lowest) / (highest - lowest))
    return scores.clip(lower=0.0, upper=1.0).fillna(0.0)


def calculate_rating_score(series: pd.Series) -> pd.Series:
    ratings = pd.to_numeric(series, errors="coerce")
    valid_ratings = ratings.dropna()

    if valid_ratings.empty:
        return pd.Series(0.0, index=series.index)

    lowest = float(valid_ratings.min())
    highest = float(valid_ratings.max())
    if lowest == highest:
        return ratings.notna().astype(float)

    scores = (ratings - lowest) / (highest - lowest)
    return scores.clip(lower=0.0, upper=1.0).fillna(0.0)


def _safe_text(value: Any, default: str = "-") -> str:
    if value is None or pd.isna(value):
        return default

    text = str(value).strip()
    return text or default


def _safe_int_text(value: Any, default: str = "-") -> str:
    number = safe_float(value, default=-1.0)
    if number < 0:
        return default
    return str(int(number)) if number.is_integer() else str(number)


def build_recommendation_reason(
    row: pd.Series,
    kebutuhan: str,
    unmet_filters: list[str] | None = None,
) -> str:
    unmet = unmet_filters or []
    if not unmet:
        return (
            f"Laptop sesuai dengan filter utama untuk kebutuhan {kebutuhan}. "
            "Spesifikasi dan skor model mendukung rekomendasi ini."
        )

    unmet_text = ", ".join(unmet)
    return (
        "Laptop ditampilkan sebagai alternatif terbaik karena belum memenuhi "
        f"filter: {unmet_text}. Sistem tetap menyertakannya berdasarkan skor "
        "model dan kedekatan spesifikasi dengan preferensi."
    )


def build_legacy_recommendation_reason(row: pd.Series, kebutuhan: str) -> str:
    processor = _safe_text(row.get("processor_series"), "processor sesuai")
    ram = _safe_int_text(row.get("ram_num"))
    storage = _safe_int_text(row.get("memory_size"))
    memory_type = _safe_text(row.get("memory_type"), "storage")
    gpu = _safe_text(row.get("gpu_type"), "GPU sesuai")
    price_matches_filter = bool(row.get("harga_sesuai_filter", True))
    price_reason = (
        "harga masih sesuai filter"
        if price_matches_filter
        else "harga menjadi alternatif terdekat dari filter"
    )

    return (
        f"Direkomendasikan untuk {kebutuhan} karena memiliki processor "
        f"{processor}, RAM {ram} GB, storage {storage} GB {memory_type}, "
        f"GPU {gpu}, dan {price_reason}."
    )


def predict_with_scores(
    model: Any, features: dict[str, Any]
) -> tuple[str, dict[str, float] | None]:
    feature_frame = pd.DataFrame([features])
    prediction = str(model.predict(feature_frame)[0])

    if not hasattr(model, "predict_proba"):
        return prediction, None

    probabilities = model.predict_proba(feature_frame)[0]
    classes = getattr(model, "classes_", [])
    scores = {
        str(label): float(probability)
        for label, probability in zip(classes, probabilities, strict=False)
    }
    return prediction, scores
