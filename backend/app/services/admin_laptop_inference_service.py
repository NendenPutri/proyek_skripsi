from typing import Any

import pandas as pd
from fastapi import HTTPException

from app.schemas.admin_laptop import AdminLaptopInferenceResult, AdminLaptopInput
from app.services.data_loader import load_laptop_dataset
from app.services.model_info_service import load_model_metadata
from app.services.model_loader import load_model

VALID_LABELS = {
    "Administrasi/Perkantoran",
    "Programming",
    "Desain Grafis",
    "Editing Video",
}

CATALOG_FIELDS = [
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
]

DEFAULT_MODEL_FEATURES = [
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


def to_python_value(value: Any) -> Any:
    """Convert NumPy/Pandas scalar values and NaN to plain Python values."""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def get_model_feature_names() -> list[str]:
    """Return pipeline feature names from model metadata."""
    metadata = load_model_metadata()
    features = metadata.get("fitur_model")
    classes = metadata.get("kelas")

    if not isinstance(features, list) or not all(isinstance(item, str) for item in features):
        raise HTTPException(
            status_code=500,
            detail="Metadata model tidak memiliki daftar fitur_model yang valid.",
        )
    if features != DEFAULT_MODEL_FEATURES:
        raise HTTPException(
            status_code=500,
            detail="Metadata fitur model tidak sesuai dengan pipeline backend saat ini.",
        )
    if not isinstance(classes, list) or not set(classes).issubset(VALID_LABELS):
        raise HTTPException(
            status_code=500,
            detail="Metadata kelas model tidak sesuai dengan label kebutuhan yang valid.",
        )
    return features


def normalize_admin_laptop_input(payload: AdminLaptopInput) -> dict[str, Any]:
    """Normalize admin laptop input before inference."""
    raw_data = payload.model_dump()
    normalized: dict[str, Any] = {}

    for field in CATALOG_FIELDS:
        value = raw_data.get(field)
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                value = None
        normalized[field] = to_python_value(value)

    if normalized["touch_screen"] is not None:
        normalized["touchscreen_label"] = "Yes" if normalized["touch_screen"] else "No"

    return normalized


def get_allowed_feature_values(feature_names: list[str]) -> dict[str, set[str]]:
    """Build allowed enum values for model features from the prepared dataset."""
    dataset = load_laptop_dataset()
    allowed_values: dict[str, set[str]] = {}

    missing_columns = [feature for feature in feature_names if feature not in dataset.columns]
    if missing_columns:
        raise HTTPException(
            status_code=500,
            detail=(
                "Dataset tidak memiliki kolom fitur model: "
                + ", ".join(missing_columns)
                + "."
            ),
        )

    for feature in feature_names:
        values = dataset[feature].dropna().astype(str).str.strip()
        allowed_values[feature] = {value for value in values.unique().tolist() if value}

    return allowed_values


def validate_feature_enums(
    model_features: dict[str, str],
    allowed_values: dict[str, set[str]],
) -> None:
    """Reject unknown enum values before sending data into the pipeline."""
    invalid_fields = []
    for feature, value in model_features.items():
        if value not in allowed_values.get(feature, set()):
            invalid_fields.append(f"{feature}={value}")

    if invalid_fields:
        raise HTTPException(
            status_code=422,
            detail="Nilai enum tidak dikenal: " + ", ".join(invalid_fields) + ".",
        )


def build_pipeline_features(payload: AdminLaptopInput) -> dict[str, str]:
    """Map normalized input to the exact feature dictionary expected by the pipeline."""
    feature_names = get_model_feature_names()
    normalized = normalize_admin_laptop_input(payload)
    model_features: dict[str, str] = {}

    missing_features = []
    for feature in feature_names:
        value = normalized.get(feature)
        if value is None or value == "":
            missing_features.append(feature)
        else:
            model_features[feature] = str(value)

    if missing_features:
        raise HTTPException(
            status_code=422,
            detail="Fitur model wajib belum lengkap: " + ", ".join(missing_features) + ".",
        )

    validate_feature_enums(model_features, get_allowed_feature_values(feature_names))
    return model_features


def _get_model_classes(model: Any) -> list[str] | None:
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        for step in reversed(list(model.named_steps.values())):
            classes = getattr(step, "classes_", None)
            if classes is not None:
                break
    if classes is None:
        return None
    return [str(to_python_value(value)) for value in classes]


def _run_predict(model: Any, features_frame: pd.DataFrame) -> str:
    try:
        prediction = model.predict(features_frame)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Pipeline model gagal melakukan prediksi.",
        ) from exc

    if len(prediction) == 0:
        raise HTTPException(
            status_code=500,
            detail="Pipeline model tidak mengembalikan hasil prediksi.",
        )

    predicted_label = str(to_python_value(prediction[0]))
    if predicted_label not in VALID_LABELS:
        raise HTTPException(
            status_code=500,
            detail="Hasil prediksi model berada di luar label kebutuhan yang valid.",
        )
    return predicted_label


def _run_predict_proba(
    model: Any,
    features_frame: pd.DataFrame,
    predicted_label: str,
) -> tuple[float | None, dict[str, float] | None]:
    if not hasattr(model, "predict_proba"):
        return None, None

    try:
        probabilities = model.predict_proba(features_frame)
    except AttributeError:
        return None, None
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Pipeline model gagal menghitung probabilitas prediksi.",
        ) from exc

    if len(probabilities) == 0:
        return None, None

    classes = _get_model_classes(model)
    row = [float(to_python_value(value)) for value in probabilities[0]]
    if not classes or len(classes) != len(row):
        return None, None

    class_probabilities = {
        class_name: probability for class_name, probability in zip(classes, row, strict=True)
    }
    confidence = class_probabilities.get(predicted_label)
    return confidence, class_probabilities


def predict_admin_laptop(payload: AdminLaptopInput) -> AdminLaptopInferenceResult:
    """Run inference for a new admin laptop without saving it."""
    normalized = normalize_admin_laptop_input(payload)
    model_features = build_pipeline_features(payload)
    feature_names = get_model_feature_names()
    features_frame = pd.DataFrame([model_features], columns=feature_names)
    model = load_model()

    predicted_label = _run_predict(model, features_frame)
    confidence, class_probabilities = _run_predict_proba(
        model,
        features_frame,
        predicted_label,
    )

    catalog = {field: to_python_value(normalized.get(field)) for field in CATALOG_FIELDS}
    return AdminLaptopInferenceResult(
        catalog=catalog,
        model_features=model_features,
        predicted_label=predicted_label,
        prediction_confidence=confidence,
        class_probabilities=class_probabilities,
    )
