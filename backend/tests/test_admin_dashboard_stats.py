from collections.abc import Iterator

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Admin, Laptop
from app.db.session import get_db
from app.services import dashboard_service, public_catalog_service
from app.services.auth_service import get_current_admin
from main import app


def laptop_row(
    model: str = "Admin Laptop",
    brand_name: str = "AdminBrand",
    is_active: bool = True,
    predicted_category: str = "Programming",
    source: str = "admin",
) -> Laptop:
    return Laptop(
        model=model,
        brand_name=brand_name,
        price=5000000,
        price_original=5000000,
        price_currency="IDR",
        price_idr=5000000,
        rating=4.7,
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
        prediction_confidence=0.9,
        source=source,
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
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_dashboard_stats_without_token_is_rejected():
    app.dependency_overrides.clear()
    response = TestClient(app).get("/api/admin/dashboard/stats")

    assert response.status_code == 401
    assert response.json()["success"] is False


def test_dashboard_stats_contract_and_four_categories(client):
    response = client.get("/api/admin/dashboard/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Statistik dashboard berhasil diambil"
    assert set(body["data"]) == {"category_distribution"}
    assert [item["category"] for item in body["data"]["category_distribution"]] == [
        "Administrasi/Perkantoran",
        "Programming",
        "Desain Grafis",
        "Editing Video",
    ]


def test_dashboard_stats_active_laptops_are_counted(client, db_session):
    db_session.add(laptop_row(model="Active Laptop", predicted_category="Programming"))
    db_session.commit()

    response = client.get("/api/admin/dashboard/stats")
    category_counts = {
        item["category"]: item["count"]
        for item in response.json()["data"]["category_distribution"]
    }

    assert category_counts["Programming"] > 0


def test_dashboard_stats_inactive_database_laptops_are_not_counted(client, db_session):
    baseline_response = client.get("/api/admin/dashboard/stats")
    baseline_counts = {
        item["category"]: item["count"]
        for item in baseline_response.json()["data"]["category_distribution"]
    }
    db_session.add(laptop_row(model="Active Laptop", predicted_category="Programming"))
    db_session.add(
        laptop_row(
            model="Inactive Laptop",
            brand_name="InactiveBrand",
            is_active=False,
            predicted_category="Editing Video",
        )
    )
    db_session.commit()

    response = client.get("/api/admin/dashboard/stats")
    category_counts = {
        item["category"]: item["count"]
        for item in response.json()["data"]["category_distribution"]
    }

    assert category_counts["Editing Video"] == baseline_counts["Editing Video"]


def test_dashboard_stats_deduplicates_csv_and_mysql_rows(client, db_session):
    csv_row = pd.read_csv("data/laptops_backend_ready.csv").iloc[0]
    csv_category = str(csv_row["label_kebutuhan"])
    replacement_category = (
        "Programming"
        if csv_category != "Programming"
        else "Administrasi/Perkantoran"
    )
    db_session.add(
        laptop_row(
            model=str(csv_row["model"]),
            brand_name=str(csv_row["brand_name"]),
            predicted_category=replacement_category,
        )
    )
    db_session.commit()

    baseline = public_catalog_service.merge_csv_and_mysql_laptops(None)
    merged = public_catalog_service.merge_csv_and_mysql_laptops(db_session)

    response = client.get("/api/admin/dashboard/stats")
    category_counts = {
        item["category"]: item["count"]
        for item in response.json()["data"]["category_distribution"]
    }

    assert len(merged) == len(baseline)
    assert category_counts[replacement_category] >= 1


def test_dashboard_stats_empty_data(monkeypatch, client):
    monkeypatch.setattr(
        dashboard_service,
        "merge_csv_and_mysql_laptops",
        lambda db: pd.DataFrame(),
    )

    response = client.get("/api/admin/dashboard/stats")
    data = response.json()["data"]

    assert response.status_code == 200
    assert all(item["count"] == 0 for item in data["category_distribution"])


def test_dashboard_stats_database_failure_uses_csv_only(client, monkeypatch):
    baseline = public_catalog_service.merge_csv_and_mysql_laptops(None)

    def fail_public_laptops(db):
        raise SQLAlchemyError("db failed")

    monkeypatch.setattr(
        public_catalog_service,
        "list_active_laptops_for_public",
        fail_public_laptops,
    )

    response = client.get("/api/admin/dashboard/stats")
    total = sum(
        item["count"]
        for item in response.json()["data"]["category_distribution"]
    )

    assert response.status_code == 200
    assert total == len(baseline)
