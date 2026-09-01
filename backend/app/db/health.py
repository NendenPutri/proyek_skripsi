from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine


def check_database_connection() -> dict[str, object]:
    """Check whether the configured database can execute a simple query."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        return {
            "available": False,
            "message": "Database tidak dapat dihubungi.",
            "error": exc.__class__.__name__,
        }

    return {
        "available": True,
        "message": "Database siap digunakan.",
        "error": None,
    }
