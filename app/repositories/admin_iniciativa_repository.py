from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.iniciativa_horario_model import IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.organizador_model import Organizador
from app.models.tag_model import Tag
from app.utils.exceptions import ResourceNotFound


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
            selectinload(Iniciativa.descricoes_extras),
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
        query = self.db.query(Iniciativa).options(
            selectinload(Iniciativa.organizador),
            selectinload(Iniciativa.horarios),
            selectinload(Iniciativa.tags),
            selectinload(Iniciativa.descricoes_extras),
        )
        if not allow_deleted:
            query = query.filter(Iniciativa.deletado_em.is_(None))
        return query.filter(Iniciativa.id == iniciativa_id).first()

    def get_by_id_active(self, iniciativa_id: str) -> Iniciativa:
        obj = (
            self.db.query(Iniciativa)
            .options(
                selectinload(Iniciativa.organizador),
                selectinload(Iniciativa.horarios),
                selectinload(Iniciativa.tags),
            )
            .filter(
                Iniciativa.id == iniciativa_id,
                Iniciativa.deletado_em.is_(None),
            )
            .first()
        )
        if not obj:
            raise ResourceNotFound("Iniciativa não encontrada")
        return obj

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

    def update_partial(
        self,
        iniciativa_id: str,
        data: Dict[str, Any],
        editado_por: Optional[str] = None,
    ) -> Iniciativa:
        """
        Aplica alterações parciais na Iniciativa.
        - Campos simples: atualiza somente os presentes em `data`.
        - tags_ids: substitui o conjunto de tags.
        - horarios: substitui a lista de horários (se fornecida).
        - 404: se não existir ou estiver soft-deletada.
        """
        obj = self.get_by_id_active(iniciativa_id)

        campos_simples = (
            "titulo",
            "descricao",
            "link",
            "destaque",
            "local",
            "imagem_url",
            "organizador_id",
        )
        for campo in campos_simples:
            if campo in data and data[campo] is not None:
                setattr(obj, campo, data[campo])

        if "tags_ids" in data and data["tags_ids"] is not None:
            tags = self.db.query(Tag).filter(Tag.id.in_(data["tags_ids"])).all()
            obj.tags = tags

        if "horarios" in data and data["horarios"] is not None:
            for h in list(obj.horarios):
                self.db.delete(h)
            self.db.flush()
            for h in data["horarios"]:
                obj.horarios.append(
                    IniciativaHorario(
                        data_evento=h.get("data_evento"),
                        hora_inicio=h.get("hora_inicio"),
                        hora_fim=h.get("hora_fim"),
                        tipo=h.get("tipo"),
                    )
                )

        obj.editado_em = func.now()
        if editado_por:
            obj.editado_por = editado_por

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj
