import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from scripts import create_admin as create_admin_script
from app.core import security
from app.core.config import get_settings
from app.db.base import Base
from app.db.models import Admin
from app.db.session import get_db
from app.repositories.admin_repository import create_admin
from app.schemas.auth import AdminResponse
from main import app


class FakeBcrypt:
    @staticmethod
    def gensalt():
        return b"test-salt"

    @staticmethod
    def hashpw(password: bytes, salt: bytes):
        digest = hashlib.sha256(salt + password).hexdigest().encode("ascii")
        return b"$2b$test$" + digest

    @staticmethod
    def checkpw(password: bytes, password_hash: bytes):
        return FakeBcrypt.hashpw(password, b"test-salt") == password_hash


def build_test_token(payload: dict, secret: str = "test-secret") -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode()
    ).rstrip(b"=").decode("ascii")
    encoded_payload = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    ).rstrip(b"=").decode("ascii")
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


@pytest.fixture()
def db_session(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    monkeypatch.setattr(security, "_load_bcrypt", lambda: FakeBcrypt)
    get_settings.cache_clear()

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
        get_settings.cache_clear()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_create_admin_success(db_session):
    admin = create_admin(
        db_session,
        name="Admin Utama",
        email="ADMIN@example.com",
        password="secret123",
    )

    assert admin.id is not None
    assert admin.email == "admin@example.com"
    assert admin.password_hash != "secret123"
    assert security.verify_password("secret123", admin.password_hash)


def test_create_admin_duplicate_email(db_session):
    create_admin(db_session, "Admin", "admin@example.com", "secret123")

    with pytest.raises(ValueError):
        create_admin(db_session, "Admin Lain", "admin@example.com", "secret456")


def test_login_success_and_password_hash_not_returned(client, db_session):
    create_admin(db_session, "Admin", "admin@example.com", "secret123")

    response = client.post(
        "/api/admin/auth/login",
        json={"email": "admin@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["access_token"]
    assert body["data"]["token_type"] == "bearer"
    assert body["data"]["admin"]["email"] == "admin@example.com"
    assert "password_hash" not in body["data"]["admin"]
    assert "password_hash" not in body["data"]


def test_login_wrong_password(client, db_session):
    create_admin(db_session, "Admin", "admin@example.com", "secret123")

    response = client.post(
        "/api/admin/auth/login",
        json={"email": "admin@example.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json()["success"] is False


def test_login_email_not_found(client):
    response = client.post(
        "/api/admin/auth/login",
        json={"email": "missing@example.com", "password": "secret123"},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Email atau password tidak valid."


def test_login_inactive_admin(client, db_session):
    admin = create_admin(db_session, "Admin", "admin@example.com", "secret123")
    admin.is_active = False
    db_session.commit()

    response = client.post(
        "/api/admin/auth/login",
        json={"email": "admin@example.com", "password": "secret123"},
    )

    assert response.status_code == 403
    assert response.json()["message"] == "Akun admin tidak aktif."


def test_valid_token_can_be_decoded(db_session):
    admin = create_admin(db_session, "Admin", "admin@example.com", "secret123")

    token = security.create_access_token(str(admin.id), {"email": admin.email})
    payload = security.decode_access_token(token)

    assert payload["sub"] == str(admin.id)
    assert payload["email"] == "admin@example.com"


def test_invalid_token_is_rejected(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    get_settings.cache_clear()

    with pytest.raises(ValueError):
        security.decode_access_token("token-tidak-valid")

    get_settings.cache_clear()


def test_expired_token_is_rejected(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    get_settings.cache_clear()
    expired_token = build_test_token(
        {
            "sub": "1",
            "exp": int((datetime.now(UTC) - timedelta(minutes=1)).timestamp()),
        }
    )

    with pytest.raises(ValueError, match="kedaluwarsa"):
        security.decode_access_token(expired_token)

    get_settings.cache_clear()


def test_me_without_token(client):
    response = client.get("/api/admin/auth/me")

    assert response.status_code == 401
    assert response.json()["success"] is False


def test_me_with_token(client, db_session):
    admin = create_admin(db_session, "Admin", "admin@example.com", "secret123")
    token = security.create_access_token(str(admin.id), {"email": admin.email})

    response = client.get(
        "/api/admin/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["email"] == "admin@example.com"
    assert "password_hash" not in body["data"]


def test_me_with_invalid_token(client):
    response = client.get(
        "/api/admin/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_password_hash_not_in_admin_response_schema():
    admin = Admin(
        id=1,
        name="Admin",
        email="admin@example.com",
        password_hash="secret-hash",
        is_active=True,
    )

    response = AdminResponse.model_validate(admin).model_dump()

    assert "password_hash" not in response
    assert response["email"] == "admin@example.com"


def test_create_admin_script_handles_database_error(monkeypatch, capsys):
    class FakeDb:
        rolled_back = False
        closed = False

        def rollback(self):
            self.rolled_back = True

        def close(self):
            self.closed = True

    fake_db = FakeDb()
    monkeypatch.setattr(
        create_admin_script,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "name": "Admin",
                "email": "admin@example.com",
                "password": "secret123",
            },
        )(),
    )
    monkeypatch.setattr(create_admin_script, "SessionLocal", lambda: fake_db)
    monkeypatch.setattr(
        create_admin_script,
        "create_admin",
        lambda **kwargs: (_ for _ in ()).throw(SQLAlchemyError("db failed")),
    )

    exit_code = create_admin_script.main()
    output = capsys.readouterr().out

    assert exit_code == 1
    assert fake_db.rolled_back is True
    assert fake_db.closed is True
    assert "Database tidak dapat diakses" in output
    assert "Traceback" not in output
