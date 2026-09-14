"""add monthly layout numbering

Revision ID: ae2e80a9a526
Revises: bcac0adec0c1
Create Date: 2026-09-15 02:16:14.923057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae2e80a9a526'
down_revision: Union[str, Sequence[str], None] = 'bcac0adec0c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ============================================================
    # 1. ADD MONTHLY NUMBERING COLUMNS
    # ============================================================
    #
    # These are temporarily nullable because existing layouts
    # already exist in the database.
    #

    op.add_column(
        "layouts",
        sa.Column(
            "layout_year",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "layout_month",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "layouts",
        sa.Column(
            "layout_number",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ============================================================
    # 2. BACKFILL YEAR AND MONTH
    # ============================================================

    op.execute(
        """
        UPDATE layouts
        SET
            layout_year = EXTRACT(YEAR FROM started_at)::INTEGER,
            layout_month = EXTRACT(MONTH FROM started_at)::INTEGER
        """
    )

    # ============================================================
    # 3. BACKFILL LAYOUT NUMBER
    # ============================================================
    #
    # Number layouts independently for each:
    #
    #   line + year + month
    #
    # Ordered chronologically by started_at.
    #
    # Example:
    #
    # Line 5 / Sep 2026:
    #   first  -> 1
    #   second -> 2
    #   third  -> 3
    #
    # Line 5 / Oct 2026:
    #   first  -> 1
    #
    # Line 1 / Sep 2026:
    #   first  -> 1
    #
    # ID is used as a deterministic tie-breaker when two layouts
    # have exactly the same started_at.
    #

    op.execute(
        """
        WITH numbered_layouts AS (
            SELECT
                id,
                ROW_NUMBER() OVER (
                    PARTITION BY
                        line_id,
                        layout_year,
                        layout_month
                    ORDER BY
                        started_at ASC,
                        id ASC
                ) AS new_layout_number
            FROM layouts
        )
        UPDATE layouts AS l
        SET layout_number = nl.new_layout_number
        FROM numbered_layouts AS nl
        WHERE l.id = nl.id
        """
    )

    # ============================================================
    # 4. MAKE COLUMNS REQUIRED
    # ============================================================

    op.alter_column(
        "layouts",
        "layout_year",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "layouts",
        "layout_month",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "layouts",
        "layout_number",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # ============================================================
    # 5. DATABASE-LEVEL UNIQUENESS
    # ============================================================
    #
    # Prevent:
    #
    # Line 5 / 2026 / 9 / Layout 1
    # Line 5 / 2026 / 9 / Layout 1   <-- NOT allowed
    #
    # But allow:
    #
    # Line 5 / 2026 / 9 / Layout 1
    # Line 5 / 2026 / 10 / Layout 1
    # Line 1 / 2026 / 9 / Layout 1
    #

    op.create_unique_constraint(
        "uq_layout_line_month_number",
        "layouts",
        [
            "line_id",
            "layout_year",
            "layout_month",
            "layout_number",
        ],
    )


def downgrade() -> None:
    # ============================================================
    # 1. REMOVE UNIQUE CONSTRAINT
    # ============================================================

    op.drop_constraint(
        "uq_layout_line_month_number",
        "layouts",
        type_="unique",
    )

    # ============================================================
    # 2. REMOVE MONTHLY NUMBERING COLUMNS
    # ============================================================

    op.drop_column(
        "layouts",
        "layout_number",
    )

    op.drop_column(
        "layouts",
        "layout_month",
    )

    op.drop_column(
        "layouts",
        "layout_year",
    )