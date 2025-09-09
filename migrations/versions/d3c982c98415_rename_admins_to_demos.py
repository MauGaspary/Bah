"""rename_admins_to_demos

Revision ID: d3c982c98415
Revises: b63cadd14ef6
Create Date: 2025-09-09 16:31:31.338479

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d3c982c98415"
down_revision: Union[str, None] = "9789fd9f80ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tabela demos já existe, nada a fazer
    pass


def downgrade() -> None:
    # Nada a reverter
    pass
