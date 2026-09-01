import pandas as pd
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.admin_laptop import AdminLaptopInput
from app.services import admin_laptop_inference_service as service


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


def valid_payload() -> AdminLaptopInput:
    return AdminLaptopInput(
        model=" Lenovo V15 ",
        brand_name="Lenovo",
        price=39990,
        price_original=39990,
        price_currency="INR",
        price_idr=7598100,
        rating=4.5,
        processor="7th Gen AMD Ryzen 7 7730U",
        processor_brand="AMD",
        processor_series="Ryzen 7",
        processor_score=4,
        processor_level="High",
        ram="16 GB DDR4 RAM",
        ram_num=16,
        ram_class="High",
        memory_type="SSD",
        memory_size=512,
        storage_class="Standard",
        gpu_brand="AMD",
        gpu_type="Integrated",
        gpu_score=1,
        gpu_level="Integrated Basic",
        os="Windows 11",
        os_family="Windows",
        display_size=15.6,
        display_class="Medium",
        resolution_height=1920,
        resolution_width=1080,
        resolution_class="Full HD",
        touch_screen=False,
        touchscreen_label="Yes",
        warranty=1,
        warranty_class="1 Year",
        price_class="Low",
    )


def metadata(features=None, classes=None):
    return {
        "fitur_model": features or MODEL_FEATURES,
        "kelas": classes
        or [
            "Administrasi/Perkantoran",
            "Desain Grafis",
            "Editing Video",
            "Programming",
        ],
    }


def dataset() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "brand_name": "Lenovo",
                "processor_brand": "AMD",
                "processor_series": "Ryzen 7",
                "processor_level": "High",
                "ram_class": "High",
                "memory_type": "SSD",
                "storage_class": "Standard",
                "gpu_brand": "AMD",
                "gpu_type": "Integrated",
                "gpu_level": "Integrated Basic",
                "os_family": "Windows",
                "display_class": "Medium",
                "resolution_class": "Full HD",
                "touchscreen_label": "No",
                "warranty_class": "1 Year",
                "price_class": "Low",
            }
        ]
    )


class FakeModelWithProba:
    classes_ = [
        "Administrasi/Perkantoran",
        "Desain Grafis",
        "Editing Video",
        "Programming",
    ]

    def __init__(self):
        self.fit_called = False
        self.partial_fit_called = False

    def predict(self, features):
        assert list(features.columns) == MODEL_FEATURES
        return ["Programming"]

    def predict_proba(self, features):
        return [[0.01, 0.02, 0.03, 0.94]]

    def fit(self, *args, **kwargs):
        self.fit_called = True
        raise AssertionError("fit tidak boleh dipanggil")

    def partial_fit(self, *args, **kwargs):
        self.partial_fit_called = True
        raise AssertionError("partial_fit tidak boleh dipanggil")


class FakeModelWithoutProba:
    def predict(self, features):
        return ["Programming"]


class FailingModel:
    def predict(self, features):
        raise RuntimeError("model failed")


class InvalidLabelModel:
    def predict(self, features):
        return ["Gaming"]


@pytest.fixture()
def patch_common(monkeypatch):
    monkeypatch.setattr(service, "load_model_metadata", lambda: metadata())
    monkeypatch.setattr(service, "load_laptop_dataset", dataset)


def test_valid_input_schema():
    payload = valid_payload()

    assert payload.model == "Lenovo V15"
    assert payload.rating == 4.5


def test_schema_accepts_pandas_boolean_scalar():
    payload = AdminLaptopInput(
        **{**valid_payload().model_dump(), "touch_screen": pd.Series([False])[0]}
    )

    assert payload.touch_screen is False


def test_normalization_sets_touchscreen_label_from_boolean():
    normalized = service.normalize_admin_laptop_input(valid_payload())

    assert normalized["model"] == "Lenovo V15"
    assert normalized["touch_screen"] is False
    assert normalized["touchscreen_label"] == "No"


def test_feature_mapping_is_correct(patch_common):
    features = service.build_pipeline_features(valid_payload())

    assert list(features) == MODEL_FEATURES
    assert features["processor_series"] == "Ryzen 7"
    assert features["touchscreen_label"] == "No"


def test_prediction_success_with_confidence(monkeypatch, patch_common):
    fake_model = FakeModelWithProba()
    monkeypatch.setattr(service, "load_model", lambda: fake_model)

    result = service.predict_admin_laptop(valid_payload())

    assert result.predicted_label == "Programming"
    assert result.prediction_confidence == 0.94
    assert result.class_probabilities["Programming"] == 0.94
    assert fake_model.fit_called is False
    assert fake_model.partial_fit_called is False


def test_confidence_null_when_predict_proba_unavailable(monkeypatch, patch_common):
    monkeypatch.setattr(service, "load_model", lambda: FakeModelWithoutProba())

    result = service.predict_admin_laptop(valid_payload())

    assert result.predicted_label == "Programming"
    assert result.prediction_confidence is None
    assert result.class_probabilities is None


def test_missing_feature_raises_http_exception(monkeypatch, patch_common):
    payload = valid_payload()
    payload.ram_class = ""

    with pytest.raises(HTTPException) as exc:
        service.build_pipeline_features(payload)

    assert exc.value.status_code == 422
    assert "ram_class" in str(exc.value.detail)


def test_unknown_enum_raises_http_exception(patch_common):
    payload = valid_payload()
    payload.processor_level = "Ultra Fast"

    with pytest.raises(HTTPException) as exc:
        service.build_pipeline_features(payload)

    assert exc.value.status_code == 422
    assert "Nilai enum tidak dikenal" in str(exc.value.detail)


def test_invalid_field_type_rejected_by_schema():
    with pytest.raises(ValidationError):
        AdminLaptopInput(**{**valid_payload().model_dump(), "rating": 9})


def test_model_failure_raises_http_exception(monkeypatch, patch_common):
    monkeypatch.setattr(service, "load_model", lambda: FailingModel())

    with pytest.raises(HTTPException) as exc:
        service.predict_admin_laptop(valid_payload())

    assert exc.value.status_code == 500
    assert "gagal melakukan prediksi" in str(exc.value.detail)


def test_invalid_predicted_category_raises_http_exception(monkeypatch, patch_common):
    monkeypatch.setattr(service, "load_model", lambda: InvalidLabelModel())

    with pytest.raises(HTTPException) as exc:
        service.predict_admin_laptop(valid_payload())

    assert exc.value.status_code == 500
    assert "di luar label" in str(exc.value.detail)


def test_metadata_feature_mismatch_raises_http_exception(monkeypatch):
    monkeypatch.setattr(service, "load_model_metadata", lambda: metadata(features=["brand_name"]))

    with pytest.raises(HTTPException) as exc:
        service.get_model_feature_names()

    assert exc.value.status_code == 500
    assert "Metadata fitur model" in str(exc.value.detail)


def test_missing_dataset_feature_raises_http_exception(monkeypatch):
    monkeypatch.setattr(service, "load_model_metadata", lambda: metadata())
    monkeypatch.setattr(service, "load_laptop_dataset", lambda: pd.DataFrame())

    with pytest.raises(HTTPException) as exc:
        service.build_pipeline_features(valid_payload())

    assert exc.value.status_code == 500
    assert "Dataset tidak memiliki kolom" in str(exc.value.detail)
