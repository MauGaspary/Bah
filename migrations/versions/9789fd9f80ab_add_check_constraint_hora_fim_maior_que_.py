"""add check constraint hora fim maior que inicio real

Revision ID: 9789fd9f80ab
Revises: 2cbcc252a7b4
Create Date: 2025-09-08 22:44:17.320613

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "9789fd9f80ab"
down_revision: Union[str, None] = "2cbcc252a7b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_hora_fim_maior_que_hora_inicio",
        "iniciativa_horarios",
        "hora_fim > hora_inicio",
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_hora_fim_maior_que_hora_inicio", "iniciativa_horarios", type_="check"
    )
