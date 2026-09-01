from app.db.base import Base
from app.db.models import Admin, Laptop


def test_orm_metadata_contains_admin_and_laptop_tables():
    assert "admins" in Base.metadata.tables
    assert "laptops" in Base.metadata.tables
    assert Admin.__tablename__ == "admins"
    assert Laptop.__tablename__ == "laptops"


def test_admin_model_required_columns_and_unique_email():
    columns = Admin.__table__.columns

    assert columns["email"].unique is True
    assert columns["password_hash"].nullable is False
    assert "password" not in columns


def test_laptop_model_supports_catalog_pipeline_and_prediction_fields():
    columns = Laptop.__table__.columns

    for column_name in [
        "model",
        "brand_name",
        "price_idr",
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
        "predicted_category",
        "prediction_confidence",
        "source",
        "is_active",
    ]:
        assert column_name in columns
