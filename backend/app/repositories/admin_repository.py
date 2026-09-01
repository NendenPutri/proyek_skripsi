from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models.admin import Admin


def get_admin_by_email(db: Session, email: str) -> Admin | None:
    """Return an admin by normalized email."""
    normalized_email = email.strip().lower()
    statement = select(Admin).where(Admin.email == normalized_email)
    return db.scalar(statement)


def get_admin_by_id(db: Session, admin_id: int) -> Admin | None:
    """Return an admin by id."""
    return db.get(Admin, admin_id)


def create_admin(db: Session, name: str, email: str, password: str) -> Admin:
    """Create an admin with a bcrypt password hash."""
    normalized_email = email.strip().lower()
    if get_admin_by_email(db, normalized_email):
        raise ValueError("Admin dengan email tersebut sudah ada.")

    admin = Admin(
        name=name.strip(),
        email=normalized_email,
        password_hash=hash_password(password),
        is_active=True,
    )
    db.add(admin)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Admin dengan email tersebut sudah ada.") from exc

    db.refresh(admin)
    return admin
