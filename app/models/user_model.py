from __future__ import annotations

import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(sa.String(320), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(sa.String(120), nullable=True)

    __table_args__ = (
        sa.Index("uq_users_email_ci", sa.text("lower(email)"), unique=True),
    )
