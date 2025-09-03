"""create users table

Revision ID: c281cae5776a
Revises: 6511b434f4cd
Create Date: 2025-09-01 15:48:32.784111
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c281cae5776a"
down_revision: Union[str, None] = "6511b434f4cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(120), nullable=True),
    )

    # UNIQUE que ignora maiusc/minusc (case-insensitive)
    op.create_index(
        "uq_users_email_ci",
        "users",
        [sa.text("lower(email)")],
        unique=True,
    )

    # Seed admin
    op.execute(
        """
        INSERT INTO users (id, email, password_hash, name)
        VALUES (
            '00000000-0000-0000-0000-000000000001',
            'admin@bah.local',
            '$2b$12$1y8F3gk7oVnG6R0C7YVQDe4mG8uX8bYf6Fv8wZg1yQx9VZs5mG8i6',
            'Admin'
        )
        ON CONFLICT DO NOTHING;
    """
    )


def downgrade() -> None:
    op.drop_index("uq_users_email_ci", table_name="users")
    op.drop_table("users")
