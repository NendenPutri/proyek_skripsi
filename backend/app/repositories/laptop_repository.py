from typing import Literal

from sqlalchemy import Select, asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.db.models.laptop import Laptop

SORTABLE_FIELDS = {
    "id": Laptop.id,
    "model": Laptop.model,
    "brand_name": Laptop.brand_name,
    "price": Laptop.price,
    "rating": Laptop.rating,
    "predicted_category": Laptop.predicted_category,
    "source": Laptop.source,
    "is_active": Laptop.is_active,
    "created_at": Laptop.created_at,
    "updated_at": Laptop.updated_at,
}


def _apply_admin_filters(
    statement: Select[tuple[Laptop]],
    search: str | None = None,
    category: str | None = None,
    status_filter: Literal["all", "active", "inactive"] = "all",
    source: str | None = None,
) -> Select[tuple[Laptop]]:
    if search:
        pattern = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Laptop.model.ilike(pattern),
                Laptop.brand_name.ilike(pattern),
            )
        )
    if category:
        statement = statement.where(Laptop.predicted_category == category)
    if status_filter == "active":
        statement = statement.where(Laptop.is_active.is_(True))
    elif status_filter == "inactive":
        statement = statement.where(Laptop.is_active.is_(False))
    if source:
        statement = statement.where(Laptop.source == source)
    return statement


def list_admin_laptops(
    db: Session,
    page: int,
    limit: int,
    search: str | None = None,
    category: str | None = None,
    status_filter: Literal["all", "active", "inactive"] = "all",
    source: str | None = None,
    sort_by: str = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> tuple[list[Laptop], int]:
    """Return paginated admin laptop rows and their total count."""
    base_statement = _apply_admin_filters(
        select(Laptop),
        search=search,
        category=category,
        status_filter=status_filter,
        source=source,
    )
    count_statement = _apply_admin_filters(
        select(func.count()).select_from(Laptop),
        search=search,
        category=category,
        status_filter=status_filter,
        source=source,
    )
    total = db.scalar(count_statement) or 0

    sort_column = SORTABLE_FIELDS[sort_by]
    order_expression = asc(sort_column) if sort_order == "asc" else desc(sort_column)
    offset = (page - 1) * limit
    rows = db.scalars(
        base_statement.order_by(order_expression).offset(offset).limit(limit)
    ).all()
    return list(rows), int(total)


def list_active_laptops_for_public(db: Session) -> list[Laptop]:
    """Return active MySQL laptops that may appear in public catalog and recommendations."""
    statement = select(Laptop).where(Laptop.is_active.is_(True))
    return list(db.scalars(statement).all())


def get_laptop_by_id(db: Session, laptop_id: int) -> Laptop | None:
    """Return a laptop row by id."""
    return db.get(Laptop, laptop_id)


def find_duplicate_laptop(
    db: Session,
    brand_name: str,
    model: str,
    source: str = "admin",
    exclude_id: int | None = None,
) -> Laptop | None:
    """Find an existing admin laptop with the same brand and model."""
    statement = select(Laptop).where(
        Laptop.brand_name == brand_name,
        Laptop.model == model,
        Laptop.source == source,
    )
    if exclude_id is not None:
        statement = statement.where(Laptop.id != exclude_id)
    return db.scalar(statement)


def add_laptop(db: Session, laptop: Laptop) -> Laptop:
    """Add a laptop row to the current transaction."""
    db.add(laptop)
    db.flush()
    db.refresh(laptop)
    return laptop


def flush_laptop(db: Session, laptop: Laptop) -> Laptop:
    """Flush and refresh an existing laptop row in the current transaction."""
    db.flush()
    db.refresh(laptop)
    return laptop
