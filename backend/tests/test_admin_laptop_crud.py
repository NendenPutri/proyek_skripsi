from collections.abc import Iterator

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.db.base import Base
from app.db.models import Admin, Laptop
from app.db.session import get_db
from app.schemas.admin_laptop import AdminLaptopInferenceResult
from app.services import admin_laptop_service
from app.services.auth_service import get_current_admin
from main import app


def laptop_payload(**overrides):
    data = {
        "model": "Lenovo V15",
        "brand_name": "Lenovo",
        "price": 39990,
        "price_original": 39990,
        "price_currency": "INR",
        "price_idr": 7598100,
        "rating": 4.5,
        "processor": "7th Gen AMD Ryzen 7 7730U",
        "processor_brand": "AMD",
        "processor_series": "Ryzen 7",
        "processor_score": 4,
        "processor_level": "High",
        "ram": "16 GB DDR4 RAM",
        "ram_num": 16,
        "ram_class": "High",
        "memory_type": "SSD",
        "memory_size": 512,
        "storage_class": "Standard",
        "gpu_brand": "AMD",
        "gpu_type": "Integrated",
        "gpu_score": 1,
        "gpu_level": "Integrated Basic",
        "os": "Windows 11",
        "os_family": "Windows",
        "display_size": 15.6,
        "display_class": "Medium",
        "resolution_height": 1920,
        "resolution_width": 1080,
        "resolution_class": "Full HD",
        "touch_screen": False,
        "touchscreen_label": "No",
        "warranty": 1,
        "warranty_class": "1 Year",
        "price_class": "Low",
    }
    data.update(overrides)
    return data


def fake_inference(payload, label="Programming"):
    catalog = payload.model_dump()
    if catalog.get("touch_screen") is not None:
        catalog["touchscreen_label"] = "Yes" if catalog["touch_screen"] else "No"
    return AdminLaptopInferenceResult(
        catalog=catalog,
        model_features={
            "brand_name": catalog["brand_name"],
            "processor_brand": catalog["processor_brand"],
            "processor_series": catalog["processor_series"],
            "processor_level": catalog["processor_level"],
            "ram_class": catalog["ram_class"],
            "memory_type": catalog["memory_type"],
            "storage_class": catalog["storage_class"],
            "gpu_brand": catalog["gpu_brand"],
            "gpu_type": catalog["gpu_type"],
            "gpu_level": catalog["gpu_level"],
            "os_family": catalog["os_family"],
            "display_class": catalog["display_class"],
            "resolution_class": catalog["resolution_class"],
            "touchscreen_label": catalog["touchscreen_label"],
            "warranty_class": catalog["warranty_class"],
            "price_class": catalog["price_class"],
        },
        predicted_label=label,
        prediction_confidence=0.91,
        class_probabilities={
            "Administrasi/Perkantoran": 0.01,
            "Desain Grafis": 0.03,
            "Editing Video": 0.05,
            "Programming": 0.91,
        },
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
def client(db_session, monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    get_settings.cache_clear()

    admin = Admin(
        id=1,
        name="Admin",
        email="admin@example.com",
        password_hash="secret-hash",
        is_active=True,
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_admin] = lambda: admin
    monkeypatch.setattr(admin_laptop_service, "predict_admin_laptop", fake_inference)

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        get_settings.cache_clear()


def create_row(client, **overrides):
    return client.post("/api/admin/laptops", json=laptop_payload(**overrides))


def test_admin_laptops_without_token_is_rejected():
    app.dependency_overrides.clear()
    response = TestClient(app).get("/api/admin/laptops")

    assert response.status_code == 401


def test_create_laptop_success_category_from_model_and_saved(client, db_session):
    response = create_row(client)

    assert response.status_code == 201
    body = response.json()
    assert body["data"]["predicted_category"] == "Programming"
    assert body["data"]["prediction_confidence"] == 0.91
    assert "password_hash" not in str(body)

    rows = db_session.scalars(select(Laptop)).all()
    assert len(rows) == 1
    assert rows[0].source == "admin"
    assert rows[0].is_active is True


def test_duplicate_laptop_rejected(client):
    assert create_row(client).status_code == 201

    response = create_row(client)

    assert response.status_code == 409


def test_inference_failure_rolls_back(client, db_session, monkeypatch):
    def fail_inference(payload):
        raise HTTPException(status_code=500, detail="inferensi gagal")

    monkeypatch.setattr(admin_laptop_service, "predict_admin_laptop", fail_inference)

    response = create_row(client)

    assert response.status_code == 500
    assert db_session.scalar(select(Laptop)) is None


def test_list_laptops_pagination_search_filter_and_sorting(client):
    create_row(client, model="Lenovo V15", brand_name="Lenovo", price=3000)
    create_row(client, model="Acer Swift", brand_name="Acer", price=5000)

    response = client.get(
        "/api/admin/laptops",
        params={
            "page": 1,
            "limit": 1,
            "search": "Acer",
            "category": "Programming",
            "status": "active",
            "sort_by": "price",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["pagination"]["total"] == 1
    assert data["pagination"]["total_pages"] == 1
    assert data["items"][0]["brand_name"] == "Acer"


def test_list_inactive_laptops_can_be_filtered(client):
    created = create_row(client).json()["data"]
    client.delete(f"/api/admin/laptops/{created['id']}")

    response = client.get("/api/admin/laptops", params={"status": "inactive"})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["is_active"] is False


def test_detail_success_and_not_found(client):
    created = create_row(client).json()["data"]

    ok_response = client.get(f"/api/admin/laptops/{created['id']}")
    missing_response = client.get("/api/admin/laptops/999")

    assert ok_response.status_code == 200
    assert ok_response.json()["data"]["id"] == created["id"]
    assert missing_response.status_code == 404


def test_update_model_field_reruns_inference(client, monkeypatch):
    calls = {"count": 0}

    def counting_inference(payload):
        calls["count"] += 1
        label = "Desain Grafis" if calls["count"] > 1 else "Programming"
        return fake_inference(payload, label=label)

    monkeypatch.setattr(admin_laptop_service, "predict_admin_laptop", counting_inference)
    created = create_row(client).json()["data"]

    response = client.put(
        f"/api/admin/laptops/{created['id']}",
        json=laptop_payload(processor_level="Mid"),
    )

    assert response.status_code == 200
    assert calls["count"] == 2
    assert response.json()["data"]["predicted_category"] == "Desain Grafis"


def test_update_catalog_field_does_not_rerun_inference(client, monkeypatch):
    created = create_row(client).json()["data"]

    def fail_if_called(payload):
        raise AssertionError("Inference tidak boleh dipanggil")

    monkeypatch.setattr(admin_laptop_service, "predict_admin_laptop", fail_if_called)
    response = client.put(
        f"/api/admin/laptops/{created['id']}",
        json=laptop_payload(rating=4.0),
    )

    assert response.status_code == 200
    assert response.json()["data"]["rating"] == 4.0
    assert response.json()["data"]["predicted_category"] == "Programming"


def test_soft_delete(client):
    created = create_row(client).json()["data"]

    response = client.delete(f"/api/admin/laptops/{created['id']}")

    assert response.status_code == 200
    assert response.json()["data"]["is_active"] is False


def test_invalid_sorting_rejected(client):
    response = client.get("/api/admin/laptops", params={"sort_by": "password_hash"})

    assert response.status_code == 422
    assert "password_hash" not in str(response.json().get("data"))
