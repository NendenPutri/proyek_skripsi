from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.models.admin import Admin
from app.db.session import get_db
from app.schemas.admin_laptop import (
    AdminLaptopInput,
    AdminLaptopListResponse,
    AdminLaptopResponse,
)
from app.schemas.common import ApiResponse
from app.services.admin_laptop_service import (
    create_admin_laptop,
    get_admin_laptop_detail,
    get_admin_laptop_list,
    soft_delete_admin_laptop,
    update_admin_laptop,
)
from app.services.auth_service import get_current_admin
from app.utils.response import success_response

router = APIRouter(prefix="/admin/laptops", tags=["Admin Laptops"])


@router.get("", response_model=ApiResponse[AdminLaptopListResponse])
async def list_laptops(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    status_filter: Literal["all", "active", "inactive"] = Query(
        default="all",
        alias="status",
    ),
    source: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Return paginated admin laptop data."""
    result = get_admin_laptop_list(
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
    return success_response("Data laptop admin berhasil diambil.", result.model_dump())


@router.get("/{laptop_id}", response_model=ApiResponse[AdminLaptopResponse])
async def get_laptop(
    laptop_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Return one admin laptop detail."""
    result = get_admin_laptop_detail(db, laptop_id)
    return success_response("Detail laptop admin berhasil diambil.", result.model_dump())


@router.post("", response_model=ApiResponse[AdminLaptopResponse], status_code=201)
async def create_laptop(
    payload: AdminLaptopInput,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Create an admin laptop after model inference."""
    result = create_admin_laptop(db, payload)
    return success_response("Laptop admin berhasil ditambahkan.", result.model_dump())


@router.put("/{laptop_id}", response_model=ApiResponse[AdminLaptopResponse])
async def update_laptop(
    laptop_id: int,
    payload: AdminLaptopInput,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Update an admin laptop and rerun inference when model features change."""
    result = update_admin_laptop(db, laptop_id, payload)
    return success_response("Laptop admin berhasil diperbarui.", result.model_dump())


@router.delete("/{laptop_id}", response_model=ApiResponse[AdminLaptopResponse])
async def delete_laptop(
    laptop_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
) -> dict[str, object]:
    """Soft delete an admin laptop."""
    result = soft_delete_admin_laptop(db, laptop_id)
    return success_response("Laptop admin berhasil dinonaktifkan.", result.model_dump())
