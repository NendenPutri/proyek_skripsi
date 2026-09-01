from app.core.config import Settings


def test_settings_reads_database_and_security_values(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "mysql+pymysql://u:p@127.0.0.1:3306/test_db")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    settings = Settings()

    assert settings.database_url == "mysql+pymysql://u:p@127.0.0.1:3306/test_db"
    assert settings.jwt_secret_key == "test-secret"
    assert settings.jwt_algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30
