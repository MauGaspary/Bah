from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class Demo(Base):
    __tablename__ = "demos"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
