import argparse
import os
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.db.session import SessionLocal  # noqa: E402
from app.repositories.admin_repository import create_admin  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Buat akun admin pertama.")
    parser.add_argument("--name", default=os.getenv("ADMIN_NAME"))
    parser.add_argument("--email", default=os.getenv("ADMIN_EMAIL"))
    parser.add_argument("--password", default=os.getenv("ADMIN_PASSWORD"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing_fields = [
        field_name
        for field_name, value in {
            "name": args.name,
            "email": args.email,
            "password": args.password,
        }.items()
        if not value
    ]
    if missing_fields:
        print(
            "Gagal membuat admin. Field wajib belum diisi: "
            + ", ".join(missing_fields)
        )
        return 1

    db = SessionLocal()
    try:
        admin = create_admin(
            db=db,
            name=args.name,
            email=args.email,
            password=args.password,
        )
    except ValueError as exc:
        db.rollback()
        print(f"Gagal membuat admin. {exc}")
        return 1
    except RuntimeError as exc:
        db.rollback()
        print(f"Gagal membuat admin. {exc}")
        return 1
    except SQLAlchemyError:
        db.rollback()
        print(
            "Gagal membuat admin. Database tidak dapat diakses. "
            "Periksa DATABASE_URL, username, password, database, dan hak akses MySQL."
        )
        return 1
    finally:
        db.close()

    print(f"Admin berhasil dibuat: {admin.email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
