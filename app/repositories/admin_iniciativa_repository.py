from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from app.models import Iniciativa


class AdminIniciativaRepository:

    @staticmethod
    def list_iniciativas(
        db: Session,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        order_by: str = "criado_em",
        order_dir: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> List[Iniciativa]:
        query = select(Iniciativa)

        if q:
            query = query.filter(Iniciativa.titulo.ilike(f"%{q}%"))

        if created_from:
            query = query.filter(Iniciativa.criado_em >= created_from)

        if created_to:
            query = query.filter(Iniciativa.criado_em <= created_to)

        if order_dir == "desc":
            query = query.order_by(getattr(Iniciativa, order_by).desc())
        else:
            query = query.order_by(getattr(Iniciativa, order_by))

        return db.execute(query.offset((page - 1) * size).limit(size)).scalars().all()

    @staticmethod
    def count_iniciativas(db: Session) -> int:
        return db.query(Iniciativa).count()
