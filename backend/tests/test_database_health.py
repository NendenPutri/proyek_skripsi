from sqlalchemy.exc import SQLAlchemyError

from app.db import health as db_health
from app.services import health_service


class SuccessfulConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def execute(self, statement):
        return None


class SuccessfulEngine:
    def connect(self):
        return SuccessfulConnection()


class FailingEngine:
    def connect(self):
        raise SQLAlchemyError("database unavailable")


class ExistingPath:
    def is_file(self):
        return True


def test_database_health_success(monkeypatch):
    monkeypatch.setattr(db_health, "engine", SuccessfulEngine())

    result = db_health.check_database_connection()

    assert result["available"] is True
    assert result["error"] is None


def test_database_health_failure(monkeypatch):
    monkeypatch.setattr(db_health, "engine", FailingEngine())

    result = db_health.check_database_connection()

    assert result["available"] is False
    assert result["error"] == "SQLAlchemyError"


def test_public_health_keeps_legacy_fields_and_adds_database(monkeypatch):
    monkeypatch.setattr(health_service, "dataset_exists", lambda: True)
    monkeypatch.setattr(health_service, "model_exists", lambda: True)
    monkeypatch.setattr(health_service, "FRONTEND_OPTIONS_PATH", ExistingPath())
    monkeypatch.setattr(health_service, "MODEL_METADATA_PATH", ExistingPath())
    monkeypatch.setattr(
        health_service,
        "check_database_connection",
        lambda: {"available": True, "message": "ok", "error": None},
    )

    result = health_service.get_health_status()

    assert result["dataset_available"] is True
    assert result["model_available"] is True
    assert result["options_available"] is True
    assert result["metadata_available"] is True
    assert result["database_available"] is True
    assert result["status"] == "ready"
