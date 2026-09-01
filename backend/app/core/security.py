import base64
import binascii
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta
from typing import Any

from app.core.config import get_settings


def _load_bcrypt():
    try:
        import bcrypt
    except ModuleNotFoundError as exc:
        raise RuntimeError("Dependency bcrypt belum terinstall.") from exc

    return bcrypt


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _json_dumps(data: dict[str, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    bcrypt = _load_bcrypt()
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    if not password or not password_hash:
        return False

    bcrypt = _load_bcrypt()
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    """Create a signed JWT access token with configured expiration."""
    settings = get_settings()
    if not settings.jwt_secret_key:
        raise RuntimeError("JWT_SECRET_KEY wajib diisi.")
    if settings.jwt_algorithm != "HS256":
        raise RuntimeError("JWT_ALGORITHM yang didukung saat ini hanya HS256.")

    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_at = datetime.now(UTC) + expires_delta
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": int(expires_at.timestamp()),
    }
    if claims:
        payload.update(claims)

    header = {"alg": settings.jwt_algorithm, "typ": "JWT"}
    encoded_header = _base64url_encode(_json_dumps(header))
    encoded_payload = _base64url_encode(_json_dumps(payload))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(
        settings.jwt_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    return f"{encoded_header}.{encoded_payload}.{_base64url_encode(signature)}"


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""
    settings = get_settings()
    if not settings.jwt_secret_key:
        raise RuntimeError("JWT_SECRET_KEY wajib diisi.")
    if settings.jwt_algorithm != "HS256":
        raise RuntimeError("JWT_ALGORITHM yang didukung saat ini hanya HS256.")

    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        header = json.loads(_base64url_decode(encoded_header))
        payload = json.loads(_base64url_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError):
        raise ValueError("Token tidak valid.") from None

    if header.get("alg") != settings.jwt_algorithm or header.get("typ") != "JWT":
        raise ValueError("Token tidak valid.")

    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    expected_signature = hmac.new(
        settings.jwt_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    try:
        signature = _base64url_decode(encoded_signature)
    except (binascii.Error, ValueError):
        raise ValueError("Token tidak valid.") from None

    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Token tidak valid.")

    exp = payload.get("exp")
    try:
        expired = exp is None or int(exp) < int(datetime.now(UTC).timestamp())
    except (TypeError, ValueError):
        raise ValueError("Token tidak valid.") from None

    if expired:
        raise ValueError("Token sudah kedaluwarsa.")

    return payload
