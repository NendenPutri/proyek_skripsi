from pathlib import Path

from app.db.base import Base
from app.db import models  # noqa: F401


def test_alembic_initial_migration_exists():
    migration_path = Path("alembic/versions/20260711_0001_create_admins_laptops.py")

    assert migration_path.is_file()


def test_alembic_metadata_has_expected_tables():
    assert {"admins", "laptops"}.issubset(Base.metadata.tables)
