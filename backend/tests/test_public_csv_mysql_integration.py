from collections.abc import Iterator

import pandas as pd
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Laptop
from app.db.session import get_db
from app.services import health_service, laptop_service, public_catalog_service
from app.services import recommendation_service
from main import app


def laptop_row(
    model="Admin Laptop",
    brand_name="AdminBrand",
    is_active=True,
    predicted_category="Programming",
    price=4500000,
) -> Laptop:
    return Laptop(
        model=model,
        brand_name=brand_name,
        price=price,
        price_original=price,
        price_currency="IDR",
        price_idr=price,
        rating=4.8,
        processor="AMD Ryzen 7",
        processor_brand="AMD",
        processor_series="Ryzen 7",
        processor_score=4,
        processor_level="High",
        ram="16 GB RAM",
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
        touchscreen_label="No",
        warranty=1,
        warranty_class="1 Year",
        price_class="Low",
        predicted_category=predicted_category,
        prediction_confidence=0.98,
        prob_administrasi_perkantoran=0.01,
        prob_desain_grafis=0.01,
        prob_editing_video=0.0,
        prob_programming=0.98,
        source="admin",
        is_active=is_active,
    )


@pytest.fixture()
def db_session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session) -> Iterator[TestClient]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


class FakeRecommendationModel:
    classes_ = [
        "Administrasi/Perkantoran",
        "Desain Grafis",
        "Editing Video",
        "Programming",
    ]

    def predict(self, features):
        return ["Programming"] * len(features)

    def predict_proba(self, features):
        return [[0.01, 0.01, 0.0, 0.98]] * len(features)


def test_csv_rows_still_available(client):
    response = client.get("/api/laptops", params={"limit": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["items"]
    assert {"items", "total", "limit", "offset"}.issubset(body["data"])


def test_active_mysql_laptop_appears_in_public_laptops(client, db_session):
    db_session.add(laptop_row())
    db_session.commit()

    response = client.get("/api/laptops", params={"search": "Admin Laptop"})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["model"] == "Admin Laptop"
    assert items[0]["predicted_label"] == "Programming"


def test_inactive_mysql_laptop_is_hidden_from_public_laptops(client, db_session):
    db_session.add(laptop_row(model="Hidden Laptop", is_active=False))
    db_session.commit()

    response = client.get("/api/laptops", params={"search": "Hidden Laptop"})

    assert response.status_code == 200
    assert response.json()["data"]["items"] == []


def test_duplicate_brand_model_prioritizes_mysql(client, db_session):
    csv_row = pd.read_csv("data/laptops_backend_ready.csv").iloc[0]
    db_session.add(
        laptop_row(
            model=str(csv_row["model"]),
            brand_name=str(csv_row["brand_name"]),
            price=123456,
        )
    )
    db_session.commit()

    response = client.get(
        "/api/laptops",
        params={"search": str(csv_row["model"]), "brand": str(csv_row["brand_name"])},
    )

    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["price"] == 123456.0


def test_public_schema_has_no_nan(client, db_session):
    db_session.add(laptop_row(model="Schema Laptop"))
    db_session.commit()

    response = client.get("/api/laptops", params={"search": "Schema Laptop"})

    item = response.json()["data"]["items"][0]
    assert "model" in item
    assert item["alasan_label"] is None


def test_mysql_laptop_can_enter_recommendations(client, db_session, monkeypatch):
    db_session.add(laptop_row(model="Recommendation Admin Laptop"))
    db_session.commit()
    monkeypatch.setattr(recommendation_service, "load_model", lambda: FakeRecommendationModel())

    response = client.post(
        "/api/recommendations",
        json={
            "kebutuhan": "Programming",
            "budget_maksimal": 5000000,
            "ram_min": 8,
            "storage_min": 256,
            "brand": "AdminBrand",
            "os_family": "Windows",
            "processor_min_level": "Mid",
            "gpu_type": "Tidak wajib",
            "touch_screen": "Semua",
            "jumlah_hasil": 5,
        },
    )

    assert response.status_code == 200
    recommendations = response.json()["data"]["recommendations"]
    assert any(item["model"] == "Recommendation Admin Laptop" for item in recommendations)
    assert {"unmet_filters", "match_percentage", "is_exact_match", "alasan_rekomendasi"}.issubset(
        recommendations[0]
    )


def test_recommendation_alternative_still_works(client, monkeypatch):
    monkeypatch.setattr(recommendation_service, "load_model", lambda: FakeRecommendationModel())

    response = client.post(
        "/api/recommendations",
        json={
            "kebutuhan": "Programming",
            "budget_maksimal": 1,
            "ram_min": 96,
            "storage_min": 4000,
            "brand": "BrandTidakAda",
            "os_family": "Windows",
            "processor_min_level": "Premium",
            "gpu_type": "Dedicated",
            "touch_screen": "Yes",
            "jumlah_hasil": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["is_alternative"] is True
    assert response.json()["data"]["recommendations"]


def test_database_failure_uses_csv_only(client, monkeypatch):
    def fail_public_laptops(db):
        raise SQLAlchemyError("db failed")

    monkeypatch.setattr(public_catalog_service, "list_active_laptops_for_public", fail_public_laptops)

    response = client.get("/api/laptops", params={"limit": 1})

    assert response.status_code == 200
    assert response.json()["data"]["items"]


def test_artifact_failure_is_reported(client, monkeypatch):
    def fail_dataset():
        raise HTTPException(status_code=503, detail="Dataset laptop belum tersedia.")

    monkeypatch.setattr(laptop_service, "merge_csv_and_mysql_laptops", lambda db=None: fail_dataset())

    response = client.get("/api/laptops")

    assert response.status_code == 503
    assert response.json()["success"] is False


def test_health_keeps_legacy_fields_and_adds_component_status(client, monkeypatch):
    class ExistingPath:
        def is_file(self):
            return True

    monkeypatch.setattr(health_service, "dataset_exists", lambda: True)
    monkeypatch.setattr(health_service, "model_exists", lambda: True)
    monkeypatch.setattr(health_service, "FRONTEND_OPTIONS_PATH", ExistingPath())
    monkeypatch.setattr(health_service, "MODEL_METADATA_PATH", ExistingPath())
    monkeypatch.setattr(
        health_service,
        "check_database_connection",
        lambda: {"available": False, "message": "Database gagal.", "error": "OperationalError"},
    )

    response = client.get("/api/health")

    data = response.json()["data"]
    assert data["dataset_available"] is True
    assert data["model_available"] is True
    assert data["options_available"] is True
    assert data["metadata_available"] is True
    assert data["database_available"] is False
    assert data["database"]["error"] == "OperationalError"
