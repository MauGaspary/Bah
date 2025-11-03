"""add descricoes_extras table

Revision ID: 905d999b1dd2
Revises: f31120b21f1a
Create Date: 2025-10-07 23:15:41.329168

"""

import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

MODEL_DIMENSION = int(os.getenv("MODEL_DIMENSIONS", "1024"))


def _vector_extension_available(connection) -> bool:
    try:
        row = connection.execute(
            text("SELECT 1 FROM pg_available_extensions WHERE name = 'vector'")
        ).fetchone()
        return bool(row)
    except Exception:
        return False


# revision identifiers, used by Alembic.
revision: str = "905d999b1dd2"
down_revision: Union[str, None] = "f31120b21f1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    has_vector = _vector_extension_available(connection)
    if has_vector:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Criar tabela já com tipo adequado
    if has_vector:
        op.create_table(
            "descricoes_extras",
            sa.Column("id", sa.String(), primary_key=True, nullable=False),
            sa.Column(
                "iniciativa_id",
                sa.String(),
                sa.ForeignKey("iniciativas.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("descricao", sa.String(), nullable=False),
            sa.Column(
                "descricao_vetor", sa.TEXT(), nullable=False
            ),  # placeholder temporário
        )
        # Ajustar para VECTOR(dim)
        op.execute(
            f"ALTER TABLE descricoes_extras ALTER COLUMN descricao_vetor TYPE VECTOR({MODEL_DIMENSION}) USING descricao_vetor::VECTOR({MODEL_DIMENSION})"
        )
    else:
        op.create_table(
            "descricoes_extras",
            sa.Column("id", sa.String(), primary_key=True, nullable=False),
            sa.Column(
                "iniciativa_id",
                sa.String(),
                sa.ForeignKey("iniciativas.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("descricao", sa.String(), nullable=False),
            sa.Column("descricao_vetor", sa.Text(), nullable=False),
        )

    # Alteração já existente (mantida do autogenerate)
    op.alter_column(
        "iniciativas",
        "organizador_id",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    # Índice separado para consultas por iniciativa_id (se necessário)
    op.create_index(
        "ix_descricoes_extras_iniciativa_id", "descricoes_extras", ["iniciativa_id"]
    )


def downgrade() -> None:
    # Reverter índice e tabela
    op.drop_index("ix_descricoes_extras_iniciativa_id", table_name="descricoes_extras")
    op.drop_table("descricoes_extras")

    # Reverter alteração da coluna iniciativas.organizador_id
    op.alter_column(
        "iniciativas",
        "organizador_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
