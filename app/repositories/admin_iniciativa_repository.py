from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.descricoes_extras_model import DescricoesExtras
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
                selectinload(Iniciativa.descricoes_extras),
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
        model: Optional[object] = None,
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

        if (
            "descricoes_extras_update" in data
            and data["descricoes_extras_update"] is not None
        ):
            for extra_data in data["descricoes_extras_update"]:
                extra_id = extra_data.get("id")
                if not extra_id:
                    continue
                extra: Optional[DescricoesExtras] = (
                    self.db.query(DescricoesExtras)
                    .filter(
                        DescricoesExtras.id == extra_id,
                        DescricoesExtras.iniciativa_id == obj.id,
                    )
                    .first()
                )
                if not extra:
                    raise ResourceNotFound("Descrição extra não encontrada")

                if "descricao" in extra_data and extra_data["descricao"] is not None:
                    extra.descricao = extra_data["descricao"]
                if (
                    "descricao_vetor" in extra_data
                    and extra_data["descricao_vetor"] is not None
                ):
                    extra.descricao_vetor = extra_data["descricao_vetor"]

        if (
            "descricoes_extras_delete_ids" in data
            and data["descricoes_extras_delete_ids"] is not None
        ):
            ids_to_delete = list(set(data["descricoes_extras_delete_ids"]))
            if ids_to_delete:
                
                existing = (
                    self.db.query(DescricoesExtras.id)
                    .filter(
                        DescricoesExtras.iniciativa_id == obj.id,
                        DescricoesExtras.id.in_(ids_to_delete),
                    )
                    .all()
                )
                existing_ids = {row[0] for row in existing}

                if not existing_ids:
                    raise ResourceNotFound("Descrição extra não encontrada")

                
                (
                    self.db.query(DescricoesExtras)
                    .filter(
                        DescricoesExtras.iniciativa_id == obj.id,
                        DescricoesExtras.id.in_(existing_ids),
                    )
                    .delete(synchronize_session=False)
                )

                
                if obj.descricoes_extras:
                    obj.descricoes_extras = [
                        e for e in obj.descricoes_extras if e.id not in existing_ids
                    ]

                self.db.flush()

        if (
            "descricoes_extras_add" in data
            and data["descricoes_extras_add"] is not None
        ):
            for novo in data["descricoes_extras_add"]:
                descricao = novo.get("descricao")
                descricao_vetor = novo.get("descricao_vetor")
                if not descricao or descricao_vetor is None:
                    continue

                self.db.add(
                    DescricoesExtras(
                        iniciativa_id=obj.id,
                        descricao=descricao,
                        descricao_vetor=descricao_vetor,
                    )
                )

        obj.editado_em = func.now()
        if editado_por:
            obj.editado_por = editado_por

        self.db.add(obj)
        self.db.commit()
        
        return self.get_by_id_active(iniciativa_id)
