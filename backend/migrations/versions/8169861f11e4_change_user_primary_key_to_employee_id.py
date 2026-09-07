"""change user primary key to employee id

Revision ID: 8169861f11e4
Revises: 873e1afe7eee
Create Date: 2026-08-28 04:57:29.987523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8169861f11e4'
down_revision: Union[str, Sequence[str], None] = '873e1afe7eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add designation to users
    op.add_column(
        "users",
        sa.Column(
            "designation",
            sa.String(length=100),
            nullable=True,
        ),
    )

    # 2. Remove the foreign key from user_sessions.user_id
    op.drop_constraint(
        "user_sessions_user_id_fkey",
        "user_sessions",
        type_="foreignkey",
    )

    # 3. Add temporary employee_id to user_sessions
    op.add_column(
        "user_sessions",
        sa.Column(
            "employee_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 4. Copy the employee ID from users
    op.execute(
        """
        UPDATE user_sessions us
        SET employee_id = u.employee_id::integer
        FROM users u
        WHERE us.user_id = u.id
        """
    )

    # 5. Make the new column required
    op.alter_column(
        "user_sessions",
        "employee_id",
        nullable=False,
    )

    # 6. Remove old user_id
    op.drop_column(
        "user_sessions",
        "user_id",
    )

    # 7. Change users.employee_id from VARCHAR to INTEGER
    op.alter_column(
        "users",
        "employee_id",
        existing_type=sa.String(length=50),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="employee_id::integer",
    )

    # 8. Remove old users primary key
    op.drop_constraint(
        "users_pkey",
        "users",
        type_="primary",
    )

    # 9. Make employee_id the new primary key
    op.create_primary_key(
        "users_pkey",
        "users",
        ["employee_id"],
    )

    # 10. Create new foreign key
    op.create_foreign_key(
        "user_sessions_employee_id_fkey",
        "user_sessions",
        "users",
        ["employee_id"],
        ["employee_id"],
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Downgrade is intentionally disabled for this migration."
    )
