from typing import Any

import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.model_loader import load_model
from app.services.public_catalog_service import merge_csv_and_mysql_laptops
from app.services.scoring_service import (
    build_recommendation_reason,
    calculate_price_score,
    calculate_rating_score,
    get_processor_level_score,
    safe_float,
)

NEED_LABELS = [
    "Administrasi/Perkantoran",
    "Programming",
    "Desain Grafis",
    "Editing Video",
]

MODEL_FEATURES = [
    "brand_name",
    "processor_brand",
    "processor_series",
    "processor_level",
    "ram_class",
    "memory_type",
    "storage_class",
    "gpu_brand",
    "gpu_type",
    "gpu_level",
    "os_family",
    "display_class",
    "resolution_class",
    "touchscreen_label",
    "warranty_class",
    "price_class",
]

OUTPUT_COLUMNS = [
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
]

ALTERNATIVE_MESSAGE = (
    "Tidak ditemukan laptop yang memenuhi semua kriteria. Sistem menampilkan "
    "alternatif terbaik dengan beberapa filter yang dilonggarkan."
)


def _is_specific(value: str | None, ignored: set[str] | None = None) -> bool:
    ignored_values = ignored or {"Semua"}
    return value is not None and value.strip() not in ignored_values


def _filter_equals(
    dataset: pd.DataFrame,
    column: str,
    value: str | None,
    ignored: set[str] | None = None,
) -> pd.DataFrame:
    if not _is_specific(value, ignored) or column not in dataset.columns:
        return dataset

    return dataset[dataset[column].astype(str).str.lower() == value.strip().lower()]


def _filter_numeric_min(
    dataset: pd.DataFrame, column: str, minimum: int | float | None
) -> pd.DataFrame:
    if minimum is None or column not in dataset.columns:
        return dataset

    values = pd.to_numeric(dataset[column], errors="coerce")
    return dataset[values >= minimum]


def _price_column(dataset: pd.DataFrame) -> str:
    if "price_idr" in dataset.columns:
        return "price_idr"
    return "price"


def _filter_by_kebutuhan(dataset: pd.DataFrame, kebutuhan: str) -> pd.DataFrame:
    matches = pd.Series(False, index=dataset.index)
    if "label_kebutuhan" in dataset.columns:
        matches = matches | (dataset["label_kebutuhan"] == kebutuhan)
    if "predicted_label" in dataset.columns:
        matches = matches | (dataset["predicted_label"] == kebutuhan)

    if not matches.any():
        return dataset
    return dataset[matches]


def _apply_request_filters(
    dataset: pd.DataFrame, request: RecommendationRequest
) -> pd.DataFrame:
    filtered = dataset.copy()

    price_column = _price_column(filtered)
    if request.budget_maksimal is not None and price_column in filtered.columns:
        prices = pd.to_numeric(filtered[price_column], errors="coerce")
        filtered = filtered[prices <= request.budget_maksimal]

    filtered = _filter_numeric_min(filtered, "ram_num", request.ram_min)
    filtered = _filter_numeric_min(filtered, "memory_size", request.storage_min)
    filtered = _filter_equals(filtered, "brand_name", request.brand)
    filtered = _filter_equals(filtered, "os_family", request.os_family)
    filtered = _filter_equals(
        filtered,
        "gpu_type",
        request.gpu_type,
        ignored={"Semua", "Tidak wajib"},
    )
    filtered = _filter_equals(filtered, "touchscreen_label", request.touch_screen)

    if (
        _is_specific(request.processor_min_level)
        and "processor_level" in filtered.columns
    ):
        requested_level = get_processor_level_score(request.processor_min_level)
        if requested_level > 0:
            scores = filtered["processor_level"].map(get_processor_level_score)
            filtered = filtered[scores >= requested_level]
        else:
            filtered = _filter_equals(
                filtered, "processor_level", request.processor_min_level
            )

    return _filter_by_kebutuhan(filtered, request.kebutuhan)


def _build_fallback_dataset(
    dataset: pd.DataFrame, request: RecommendationRequest
) -> pd.DataFrame:
    fallback = dataset.copy()

    price_column = _price_column(fallback)
    if request.budget_maksimal is not None and price_column in fallback.columns:
        prices = pd.to_numeric(fallback[price_column], errors="coerce")
        budget_fallback = fallback[prices <= request.budget_maksimal]
        if not budget_fallback.empty:
            fallback = budget_fallback

    matched = _filter_by_kebutuhan(fallback, request.kebutuhan)
    if not matched.empty:
        fallback = matched

    return fallback


def _safe_number(value: Any) -> float | None:
    number = safe_float(value, default=float("nan"))
    if pd.isna(number):
        return None
    return number


def _matches_text(value: Any, expected: str | None) -> bool:
    if not _is_specific(expected):
        return True
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() == expected.strip().lower()


def _matches_numeric_min(value: Any, minimum: int | float | None) -> bool:
    if minimum is None:
        return True
    number = _safe_number(value)
    return number is not None and number >= minimum


def _matches_processor_level(value: Any, minimum_level: str | None) -> bool:
    if not _is_specific(minimum_level):
        return True

    requested_score = get_processor_level_score(minimum_level)
    current_score = get_processor_level_score(value)
    if requested_score > 0:
        return current_score >= requested_score

    return _matches_text(value, minimum_level)


def _matches_kebutuhan(row: pd.Series, kebutuhan: str) -> bool:
    values = [
        row.get("label_kebutuhan"),
        row.get("predicted_label"),
        row.get("backend_predicted_label"),
    ]
    return any(_matches_text(value, kebutuhan) for value in values)


def _build_unmet_filters(row: pd.Series, request: RecommendationRequest) -> list[str]:
    unmet: list[str] = []

    if not _matches_kebutuhan(row, request.kebutuhan):
        unmet.append("Kebutuhan")

    price_column = "price_idr" if "price_idr" in row.index else "price"
    if request.budget_maksimal is not None:
        price_value = row.get(price_column)
        if (
            not _matches_numeric_min(price_value, 0)
            or safe_float(price_value) > safe_float(request.budget_maksimal)
        ):
            unmet.append("Budget Maksimal")

    if not _matches_numeric_min(row.get("ram_num"), request.ram_min):
        unmet.append("RAM Minimum")
    if not _matches_numeric_min(row.get("memory_size"), request.storage_min):
        unmet.append("Storage Minimum")
    if not _matches_text(row.get("brand_name"), request.brand):
        unmet.append("Brand")
    if not _matches_text(row.get("os_family"), request.os_family):
        unmet.append("Sistem Operasi")
    if not _matches_processor_level(row.get("processor_level"), request.processor_min_level):
        unmet.append("Level Processor Minimum")
    if _is_specific(request.gpu_type, ignored={"Semua", "Tidak wajib"}) and not _matches_text(row.get("gpu_type"), request.gpu_type):
        unmet.append("Tipe GPU")
    if not _matches_text(row.get("touchscreen_label"), request.touch_screen):
        unmet.append("Touch Screen")

    return unmet


def _active_filter_count(request: RecommendationRequest) -> int:
    count = 1
    if request.budget_maksimal is not None:
        count += 1
    if request.ram_min is not None:
        count += 1
    if request.storage_min is not None:
        count += 1
    if _is_specific(request.brand):
        count += 1
    if _is_specific(request.os_family):
        count += 1
    if _is_specific(request.processor_min_level):
        count += 1
    if _is_specific(request.gpu_type, ignored={"Semua", "Tidak wajib"}):
        count += 1
    if _is_specific(request.touch_screen):
        count += 1
    return count


def _match_percentage(unmet_filters: list[str], active_filter_count: int) -> float:
    if active_filter_count <= 0:
        return 100.0
    matched_count = max(active_filter_count - len(unmet_filters), 0)
    percentage = round((matched_count / active_filter_count) * 100, 1)
    if unmet_filters and percentage >= 100:
        return 99.0
    return percentage


def _build_model_input(dataset: pd.DataFrame) -> pd.DataFrame:
    model_input = pd.DataFrame(index=dataset.index)
    for feature in MODEL_FEATURES:
        if feature in dataset.columns:
            model_input[feature] = dataset[feature].fillna("").astype(str)
        else:
            model_input[feature] = ""
    return model_input


def _predict_candidates(
    model: Any, candidates: pd.DataFrame, kebutuhan: str
) -> tuple[pd.Series, pd.Series]:
    default_labels = pd.Series("", index=candidates.index, dtype=object)
    default_confidence = pd.Series(0.0, index=candidates.index, dtype=float)

    if candidates.empty:
        return default_labels, default_confidence

    model_input = _build_model_input(candidates)

    try:
        predictions = pd.Series(
            model.predict(model_input),
            index=candidates.index,
        ).astype(str)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Model gagal melakukan prediksi pada kandidat laptop.",
        ) from exc

    if not hasattr(model, "predict_proba"):
        return predictions, default_confidence

    try:
        probabilities = model.predict_proba(model_input)
    except Exception:
        return predictions, default_confidence

    classes = [str(label) for label in getattr(model, "classes_", [])]
    if kebutuhan not in classes:
        return predictions, default_confidence

    class_index = classes.index(kebutuhan)
    probability_frame = pd.DataFrame(probabilities, index=candidates.index)
    confidence = probability_frame.iloc[:, class_index].astype(float)
    return predictions, confidence.fillna(0.0).clip(lower=0.0, upper=1.0)


def _class_match_score(
    candidates: pd.DataFrame, predicted_labels: pd.Series, kebutuhan: str
) -> pd.Series:
    score = pd.Series(0.0, index=candidates.index)

    if "label_kebutuhan" in candidates.columns:
        score = score.mask(candidates["label_kebutuhan"] == kebutuhan, 1.0)
    if "predicted_label" in candidates.columns:
        score = score.mask(candidates["predicted_label"] == kebutuhan, 1.0)

    return score.mask(predicted_labels == kebutuhan, 1.0)


def _safe_output_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()
    return value


def _build_recommendation_items(
    candidates: pd.DataFrame,
    kebutuhan: str,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for _, row in candidates.iterrows():
        item = {column: _safe_output_value(row.get(column)) for column in OUTPUT_COLUMNS}
        item["backend_predicted_label"] = _safe_output_value(
            row.get("backend_predicted_label")
        )
        item["backend_confidence"] = safe_float(row.get("backend_confidence"))
        item["final_score"] = safe_float(row.get("final_score"))
        unmet_filters = row.get("unmet_filters", [])
        if not isinstance(unmet_filters, list):
            unmet_filters = []
        item["unmet_filters"] = unmet_filters
        item["match_percentage"] = safe_float(row.get("match_percentage"))
        item["is_exact_match"] = bool(row.get("is_exact_match", False))
        item["alasan_rekomendasi"] = build_recommendation_reason(
            row,
            kebutuhan,
            unmet_filters,
        )
        items.append(item)

    return items


def recommend_laptops(
    request: RecommendationRequest,
    db: Session | None = None,
) -> RecommendationResponse:
    """Generate ranked laptop recommendations from user preferences."""
    if request.kebutuhan not in NEED_LABELS:
        raise HTTPException(
            status_code=422,
            detail="Label kebutuhan tidak valid.",
        )

    dataset = merge_csv_and_mysql_laptops(db)
    model = load_model()

    filtered = _apply_request_filters(dataset, request)
    is_alternative = filtered.empty
    candidates = filtered

    if is_alternative:
        candidates = _build_fallback_dataset(dataset, request)

    if candidates.empty:
        raise HTTPException(
            status_code=404,
            detail="Tidak ada laptop yang dapat direkomendasikan dari dataset.",
        )

    candidates = candidates.copy()
    price_column = _price_column(candidates)
    if request.budget_maksimal is not None and price_column in candidates.columns:
        candidate_prices = pd.to_numeric(candidates[price_column], errors="coerce")
        candidates["harga_sesuai_filter"] = candidate_prices <= request.budget_maksimal
    else:
        candidates["harga_sesuai_filter"] = True

    backend_labels, backend_confidence = _predict_candidates(
        model, candidates, request.kebutuhan
    )
    candidates["backend_predicted_label"] = backend_labels
    candidates["backend_confidence"] = backend_confidence
    active_filter_count = _active_filter_count(request)
    unmet_filters_by_index = {
        index: _build_unmet_filters(row, request)
        for index, row in candidates.iterrows()
    }
    candidates["unmet_filters"] = pd.Series(unmet_filters_by_index)
    candidates["match_percentage"] = candidates["unmet_filters"].map(
        lambda filters: _match_percentage(filters, active_filter_count)
    )
    candidates["is_exact_match"] = candidates["unmet_filters"].map(lambda filters: len(filters) == 0)

    class_score = _class_match_score(candidates, backend_labels, request.kebutuhan)
    target_probability = backend_confidence
    rating_score = calculate_rating_score(
        candidates.get("rating", pd.Series(index=candidates.index))
    )
    price_score = calculate_price_score(
        candidates.get(price_column, pd.Series(index=candidates.index))
    )
    match_score = candidates["match_percentage"].astype(float) / 100

    candidates["final_score"] = (
        (match_score * 0.45)
        + (class_score * 0.25)
        + (target_probability * 0.15)
        + (rating_score * 0.075)
        + (price_score * 0.075)
    ).fillna(0.0)

    ranked = candidates.sort_values(
        by="final_score",
        ascending=False,
        kind="mergesort",
    ).head(request.jumlah_hasil)

    message = ALTERNATIVE_MESSAGE if is_alternative else "Rekomendasi laptop berhasil dibuat."

    return RecommendationResponse(
        message=message,
        total=len(ranked),
        is_alternative=is_alternative,
        recommendations=_build_recommendation_items(ranked, request.kebutuhan),
    )


def get_recommendations(
    payload: RecommendationRequest,
    db: Session | None = None,
) -> dict[str, Any]:
    return recommend_laptops(payload, db=db).model_dump()
