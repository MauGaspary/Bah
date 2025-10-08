from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.iniciativa_horario_model import IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.organizador_model import Organizador
from app.models.tag_model import Tag


class AdminIniciativaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_iniciativas(
        self,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        order_by: str = "criado_em",
        order_dir: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> List[Iniciativa]:
        query = select(Iniciativa).options(
            selectinload(Iniciativa.organizador),
            selectinload(Iniciativa.horarios),
            selectinload(Iniciativa.tags),
        )

        filters = []

        filters.append(Iniciativa.deletado_em.is_(None))

        if q:

            tag_search = select(Tag.id).where(Tag.nome.ilike(f"%{q}%"))
            iniciativa_with_tag = (
                select(Iniciativa.id)
                .join(Iniciativa.tags)
                .where(Tag.id.in_(tag_search))
            )

            filters.append(
                or_(
                    Iniciativa.titulo.ilike(f"%{q}%"),
                    Iniciativa.descricao.ilike(f"%{q}%"),
                    Iniciativa.id.in_(iniciativa_with_tag),
                )
            )

        if created_from:
            filters.append(Iniciativa.criado_em >= created_from)

        if created_to:
            filters.append(Iniciativa.criado_em <= created_to)

        if filters:
            query = query.where(and_(*filters))

        order_column = getattr(Iniciativa, order_by, Iniciativa.criado_em)
        if order_dir == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        query = query.offset((page - 1) * size).limit(size)

        return self.db.execute(query).scalars().all()

    def get_by_id(
        self, iniciativa_id: str, allow_deleted: bool = False
    ) -> Optional[Iniciativa]:
        query = self.db.query(Iniciativa)
        if not allow_deleted:
            query = query.filter(Iniciativa.deletado_em.is_(None))
        return query.filter(Iniciativa.id == iniciativa_id).first()

    def soft_delete(self, iniciativa_id: str, deletado_por: str) -> bool:
        iniciativa = self.get_by_id(iniciativa_id, allow_deleted=True)
        if not iniciativa:
            return False

        if iniciativa.deletado_em is None:
            iniciativa.deletado_em = func.now()
            iniciativa.deletado_por = deletado_por
            self.db.commit()
            self.db.refresh(iniciativa)

        return True

    def count_iniciativas(
        self,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
    ) -> int:
        query = select(func.count(Iniciativa.id))

        filters = []

        filters.append(Iniciativa.deletado_em.is_(None))

        if q:

            tag_search = select(Tag.id).where(Tag.nome.ilike(f"%{q}%"))
            iniciativa_with_tag = (
                select(Iniciativa.id)
                .join(Iniciativa.tags)
                .where(Tag.id.in_(tag_search))
            )

            filters.append(
                or_(
                    Iniciativa.titulo.ilike(f"%{q}%"),
                    Iniciativa.descricao.ilike(f"%{q}%"),
                    Iniciativa.id.in_(iniciativa_with_tag),
                )
            )

        if created_from:
            filters.append(Iniciativa.criado_em >= created_from)

        if created_to:
            filters.append(Iniciativa.criado_em <= created_to)

        if filters:
            query = query.where(and_(*filters))

        return self.db.execute(query).scalar() or 0

    def get_iniciativa_with_relations(self, iniciativa_id: str) -> Optional[Iniciativa]:
        query = (
            select(Iniciativa)
            .options(
                selectinload(Iniciativa.organizador),
                selectinload(Iniciativa.horarios),
                selectinload(Iniciativa.tags),
            )
            .where(Iniciativa.id == iniciativa_id, Iniciativa.deletado_em.is_(None))
        )
        return self.db.execute(query).scalar_one_or_none()

    def update_iniciativa(self, iniciativa: Iniciativa, **kwargs) -> Iniciativa:
        for key, value in kwargs.items():
            if value is not None:
                setattr(iniciativa, key, value)
        self.db.commit()
        self.db.refresh(iniciativa)
        return iniciativa
