import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from app.core.paths import BACKEND_DIR

load_dotenv(BACKEND_DIR / ".env")


class Settings(BaseModel):
    app_name: str = Field(
        default_factory=lambda: os.getenv(
            "APP_NAME", "Sistem Rekomendasi Laptop API"
        )
    )
    app_version: str = Field(default_factory=lambda: os.getenv("APP_VERSION", "1.0.0"))
    api_prefix: str = Field(default_factory=lambda: os.getenv("API_PREFIX", "/api"))
    database_url: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://username:password@127.0.0.1:3306/laptopwise",
        )
    )
    jwt_secret_key: str = Field(default_factory=lambda: os.getenv("JWT_SECRET_KEY", ""))
    jwt_algorithm: str = Field(
        default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256")
    )
    access_token_expire_minutes: int = Field(
        default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "600"))
    )
    backend_cors_origins: str = Field(
        default_factory=lambda: os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
    )

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("API_PREFIX harus diawali dengan '/'.")
        return value.rstrip("/") or "/"

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value:
            raise ValueError("DATABASE_URL wajib diisi.")
        return value

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
