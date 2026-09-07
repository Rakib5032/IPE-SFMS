"""add line assignments status layout production

Revision ID: bcac0adec0c1
Revises: 8169861f11e4
Create Date: 2026-08-29 05:58:59.343961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bcac0adec0c1"
down_revision: Union[str, Sequence[str], None] = "8169861f11e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ============================================================
    # LINE ASSIGNMENTS
    # ============================================================

    op.create_table(
        "line_assignments",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "line_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "assignment_type",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "start_date",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "end_date",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["users.employee_id"],
        ),
        sa.ForeignKeyConstraint(
            ["line_id"],
            ["lines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ============================================================
    # LINE STATUSES
    # ============================================================

    op.create_table(
        "line_statuses",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "line_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "reason",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "ended_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["line_id"],
            ["lines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ============================================================
    # PRODUCTION
    # ============================================================

    op.create_table(
        "productions",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "line_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "production_date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "target",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["line_id"],
            ["lines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "line_id",
            "production_date",
            name="uq_production_line_date",
        ),
    )

    # ============================================================
    # LAYOUT MACHINES
    # ============================================================

    op.create_table(
        "layout_machines",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "layout_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "machine_number",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "machine_name",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "reason",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["layout_id"],
            ["layouts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ============================================================
    # LAYOUT - NEW COLUMNS
    # ============================================================

    # Existing layouts may already contain data.
    # Therefore these are initially nullable.

    op.add_column(
        "layouts",
        sa.Column(
            "required_machine_count",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "notes",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # ============================================================
    # LAYOUT - EXISTING COLUMNS
    # ============================================================
    #
    # IMPORTANT:
    # We intentionally DO NOT drop:
    #
    # total_machines
    # machine_status
    # status
    # duration_minutes
    # smv
    # buyer
    #
    # These existing fields contain useful layout information.
    # ============================================================

    op.alter_column(
        "layouts",
        "style",
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
    )

    op.alter_column(
        "layouts",
        "job",
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
    )

    # ============================================================
    # LINE NUMBER UNIQUE CONSTRAINT
    # ============================================================

    op.create_unique_constraint(
        "uq_lines_line_number",
        "lines",
        ["line_number"],
    )

    # ============================================================
    # USERS
    # ============================================================
    #
    # IMPORTANT:
    # Do NOT remove users.id.
    # Do NOT remove users_employee_id_key.
    #
    # Existing user data must remain untouched.
    # ============================================================


def downgrade() -> None:
    """Downgrade schema."""

    # ============================================================
    # DROP LINE NUMBER CONSTRAINT
    # ============================================================

    op.drop_constraint(
        "uq_lines_line_number",
        "lines",
        type_="unique",
    )

    # ============================================================
    # DROP NEW LAYOUT COLUMNS
    # ============================================================

    op.drop_column(
        "layouts",
        "updated_at",
    )

    op.drop_column(
        "layouts",
        "created_at",
    )

    op.drop_column(
        "layouts",
        "notes",
    )

    op.drop_column(
        "layouts",
        "is_active",
    )

    op.drop_column(
        "layouts",
        "required_machine_count",
    )

    # ============================================================
    # DROP NEW TABLES
    # ============================================================

    op.drop_table(
        "layout_machines",
    )

    op.drop_table(
        "productions",
    )

    op.drop_table(
        "line_statuses",
    )

    op.drop_table(
        "line_assignments",
    )