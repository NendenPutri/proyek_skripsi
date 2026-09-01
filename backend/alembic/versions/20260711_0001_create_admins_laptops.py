"""create admins and laptops tables

Revision ID: 20260711_0001
Revises:
Create Date: 2026-07-11 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260711_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admins_id"), "admins", ["id"], unique=False)
    op.create_index(op.f("ix_admins_email"), "admins", ["email"], unique=True)
    op.create_index(op.f("ix_admins_is_active"), "admins", ["is_active"], unique=False)

    op.create_table(
        "laptops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model", sa.String(length=255), nullable=False),
        sa.Column("brand_name", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("price_original", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("price_currency", sa.String(length=10), nullable=True),
        sa.Column("price_idr", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("processor", sa.String(length=255), nullable=True),
        sa.Column("processor_brand", sa.String(length=100), nullable=True),
        sa.Column("processor_series", sa.String(length=100), nullable=True),
        sa.Column("processor_score", sa.Float(), nullable=True),
        sa.Column("processor_level", sa.String(length=50), nullable=True),
        sa.Column("ram", sa.String(length=100), nullable=True),
        sa.Column("ram_num", sa.Integer(), nullable=True),
        sa.Column("ram_class", sa.String(length=50), nullable=True),
        sa.Column("memory_type", sa.String(length=50), nullable=True),
        sa.Column("memory_size", sa.Integer(), nullable=True),
        sa.Column("storage_class", sa.String(length=50), nullable=True),
        sa.Column("gpu_brand", sa.String(length=100), nullable=True),
        sa.Column("gpu_type", sa.String(length=50), nullable=True),
        sa.Column("gpu_score", sa.Float(), nullable=True),
        sa.Column("gpu_level", sa.String(length=100), nullable=True),
        sa.Column("os", sa.String(length=100), nullable=True),
        sa.Column("os_family", sa.String(length=50), nullable=True),
        sa.Column("display_size", sa.Float(), nullable=True),
        sa.Column("display_class", sa.String(length=50), nullable=True),
        sa.Column("resolution_height", sa.Integer(), nullable=True),
        sa.Column("resolution_width", sa.Integer(), nullable=True),
        sa.Column("resolution_class", sa.String(length=50), nullable=True),
        sa.Column("touch_screen", sa.Boolean(), nullable=True),
        sa.Column("touchscreen_label", sa.String(length=20), nullable=True),
        sa.Column("warranty", sa.Integer(), nullable=True),
        sa.Column("warranty_class", sa.String(length=50), nullable=True),
        sa.Column("price_class", sa.String(length=50), nullable=True),
        sa.Column("predicted_category", sa.String(length=100), nullable=True),
        sa.Column("prediction_confidence", sa.Float(), nullable=True),
        sa.Column("alasan_label", sa.Text(), nullable=True),
        sa.Column("prob_administrasi_perkantoran", sa.Float(), nullable=True),
        sa.Column("prob_desain_grafis", sa.Float(), nullable=True),
        sa.Column("prob_editing_video", sa.Float(), nullable=True),
        sa.Column("prob_programming", sa.Float(), nullable=True),
        sa.Column("source", sa.String(length=50), server_default="admin", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("brand_name", "model", "source", name="uq_laptops_brand_model_source"),
    )
    op.create_index(op.f("ix_laptops_id"), "laptops", ["id"], unique=False)
    op.create_index("ix_laptops_brand_name", "laptops", ["brand_name"], unique=False)
    op.create_index("ix_laptops_model", "laptops", ["model"], unique=False)
    op.create_index("ix_laptops_predicted_category", "laptops", ["predicted_category"], unique=False)
    op.create_index("ix_laptops_is_active", "laptops", ["is_active"], unique=False)
    op.create_index("ix_laptops_source", "laptops", ["source"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_laptops_source", table_name="laptops")
    op.drop_index("ix_laptops_is_active", table_name="laptops")
    op.drop_index("ix_laptops_predicted_category", table_name="laptops")
    op.drop_index("ix_laptops_model", table_name="laptops")
    op.drop_index("ix_laptops_brand_name", table_name="laptops")
    op.drop_index(op.f("ix_laptops_id"), table_name="laptops")
    op.drop_table("laptops")
    op.drop_index(op.f("ix_admins_is_active"), table_name="admins")
    op.drop_index(op.f("ix_admins_email"), table_name="admins")
    op.drop_index(op.f("ix_admins_id"), table_name="admins")
    op.drop_table("admins")
