from math import ceil
from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.laptop import Laptop
from app.repositories.laptop_repository import (
    SORTABLE_FIELDS,
    add_laptop,
    find_duplicate_laptop,
    flush_laptop,
    get_laptop_by_id,
    list_admin_laptops,
)
from app.schemas.admin_laptop import (
    AdminLaptopInput,
    AdminLaptopListResponse,
    AdminLaptopPagination,
    AdminLaptopResponse,
)
from app.services.admin_laptop_inference_service import (
    CATALOG_FIELDS,
    DEFAULT_MODEL_FEATURES,
    VALID_LABELS,
    normalize_admin_laptop_input,
    predict_admin_laptop,
    to_python_value,
)


def _serialize_laptop(laptop: Laptop) -> AdminLaptopResponse:
    data = {
        field: to_python_value(getattr(laptop, field))
        for field in CATALOG_FIELDS
        if hasattr(laptop, field)
    }
    data.update(
        {
            "id": laptop.id,
            "predicted_category": laptop.predicted_category,
            "prediction_confidence": laptop.prediction_confidence,
            "source": laptop.source,
            "is_active": laptop.is_active,
            "created_at": laptop.created_at,
            "updated_at": laptop.updated_at,
        }
    )
    return AdminLaptopResponse.model_validate(data)


def _probability_columns(class_probabilities: dict[str, float] | None) -> dict[str, float | None]:
    probabilities = class_probabilities or {}
    return {
        "prob_administrasi_perkantoran": probabilities.get("Administrasi/Perkantoran"),
        "prob_desain_grafis": probabilities.get("Desain Grafis"),
        "prob_editing_video": probabilities.get("Editing Video"),
        "prob_programming": probabilities.get("Programming"),
    }


def _build_laptop_from_payload(payload: AdminLaptopInput) -> Laptop:
    inference_result = predict_admin_laptop(payload)
    if inference_result.predicted_label not in VALID_LABELS:
        raise HTTPException(
            status_code=500,
            detail="Hasil prediksi model berada di luar label kebutuhan yang valid.",
        )

    data = {
        field: inference_result.catalog.get(field)
        for field in CATALOG_FIELDS
    }
    data.update(
        {
            "predicted_category": inference_result.predicted_label,
            "prediction_confidence": inference_result.prediction_confidence,
            "source": "admin",
            "is_active": True,
            **_probability_columns(inference_result.class_probabilities),
        }
    )
    return Laptop(**data)


def _model_features_changed(laptop: Laptop, payload: AdminLaptopInput) -> bool:
    normalized = normalize_admin_laptop_input(payload)
    for field in DEFAULT_MODEL_FEATURES:
        old_value = getattr(laptop, field)
        new_value = normalized.get(field)
        if str(to_python_value(old_value)) != str(to_python_value(new_value)):
            return True
    return False


def get_admin_laptop_list(
    db: Session,
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
    category: str | None = None,
    status_filter: Literal["all", "active", "inactive"] = "all",
    source: str | None = None,
    sort_by: str = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> AdminLaptopListResponse:
    """Return paginated admin laptops with filters and sorting."""
    if category and category not in VALID_LABELS:
        raise HTTPException(status_code=422, detail="Kategori filter tidak valid.")
    if sort_by not in SORTABLE_FIELDS:
        raise HTTPException(status_code=422, detail="Field sorting tidak valid.")

    items, total = list_admin_laptops(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category=category,
        status_filter=status_filter,
        source=source,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    total_pages = ceil(total / limit) if total else 0
    return AdminLaptopListResponse(
        items=[_serialize_laptop(item) for item in items],
        pagination=AdminLaptopPagination(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


def get_admin_laptop_detail(db: Session, laptop_id: int) -> AdminLaptopResponse:
    """Return detail for an admin laptop row."""
    laptop = get_laptop_by_id(db, laptop_id)
    if not laptop:
        raise HTTPException(status_code=404, detail="Data laptop tidak ditemukan.")
    return _serialize_laptop(laptop)


def create_admin_laptop(db: Session, payload: AdminLaptopInput) -> AdminLaptopResponse:
    """Validate, infer, and store a new admin laptop in one transaction."""
    normalized = normalize_admin_laptop_input(payload)
    if find_duplicate_laptop(db, normalized["brand_name"], normalized["model"]):
        raise HTTPException(status_code=409, detail="Laptop admin sudah ada.")

    try:
        laptop = _build_laptop_from_payload(payload)
        add_laptop(db, laptop)
        db.commit()
        db.refresh(laptop)
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Data laptop gagal disimpan.",
        ) from exc

    return _serialize_laptop(laptop)


def update_admin_laptop(
    db: Session,
    laptop_id: int,
    payload: AdminLaptopInput,
) -> AdminLaptopResponse:
    """Update an admin laptop and rerun inference only when model features change."""
    laptop = get_laptop_by_id(db, laptop_id)
    if not laptop:
        raise HTTPException(status_code=404, detail="Data laptop tidak ditemukan.")

    normalized = normalize_admin_laptop_input(payload)
    duplicate = find_duplicate_laptop(
        db,
        normalized["brand_name"],
        normalized["model"],
        exclude_id=laptop_id,
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Laptop admin sudah ada.")

    try:
        should_infer = _model_features_changed(laptop, payload)
        inference_result = predict_admin_laptop(payload) if should_infer else None
        if inference_result and inference_result.predicted_label not in VALID_LABELS:
            raise HTTPException(
                status_code=500,
                detail="Hasil prediksi model berada di luar label kebutuhan yang valid.",
            )

        for field in CATALOG_FIELDS:
            setattr(laptop, field, normalized.get(field))

        if inference_result:
            laptop.predicted_category = inference_result.predicted_label
            laptop.prediction_confidence = inference_result.prediction_confidence
            for field, value in _probability_columns(
                inference_result.class_probabilities
            ).items():
                setattr(laptop, field, value)

        flush_laptop(db, laptop)
        db.commit()
        db.refresh(laptop)
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Data laptop gagal diperbarui.",
        ) from exc

    return _serialize_laptop(laptop)


def soft_delete_admin_laptop(db: Session, laptop_id: int) -> AdminLaptopResponse:
    """Soft delete an admin laptop by marking it inactive."""
    laptop = get_laptop_by_id(db, laptop_id)
    if not laptop:
        raise HTTPException(status_code=404, detail="Data laptop tidak ditemukan.")

    try:
        laptop.is_active = False
        flush_laptop(db, laptop)
        db.commit()
        db.refresh(laptop)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Data laptop gagal dinonaktifkan.",
        ) from exc

    return _serialize_laptop(laptop)
