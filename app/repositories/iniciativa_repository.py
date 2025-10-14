from typing import List, Optional

import numpy as np
from sqlalchemy import and_, func, or_, text
from sqlalchemy.orm import Session, selectinload

from app.models.descricoes_extras_model import DescricoesExtras
from app.models.iniciativa_horario_model import IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.iniciativa_tag_model import IniciativaTag
from app.models.organizador_model import Organizador
from app.models.tag_model import Tag
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse


class IniciativaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        iniciativa_data: IniciativaCreate,
        criado_por: str,
        descricao_vetor: List[float],
    ) -> Iniciativa:

        db_iniciativa = Iniciativa(
            titulo=iniciativa_data.titulo,
            descricao=iniciativa_data.descricao,
            descricao_vetor=descricao_vetor,
            organizador_id=iniciativa_data.organizador_id,
            link=iniciativa_data.link,
            local=iniciativa_data.local,
            imagem_url=iniciativa_data.imagem_url,
            destaque=iniciativa_data.destaque,
            criado_por=criado_por,
        )

        self.db.add(db_iniciativa)
        self.db.flush()

        for horario_data in iniciativa_data.horarios:
            db_horario = IniciativaHorario(
                iniciativa_id=db_iniciativa.id,
                data_evento=horario_data.data_evento,
                hora_inicio=horario_data.hora_inicio,
                hora_fim=horario_data.hora_fim,
                tipo=horario_data.tipo,
            )
            self.db.add(db_horario)

        if iniciativa_data.tag_ids:
            for tag_id in iniciativa_data.tag_ids:
                db_iniciativa_tag = IniciativaTag(
                    iniciativa_id=db_iniciativa.id, tag_id=tag_id
                )
                self.db.add(db_iniciativa_tag)

        if iniciativa_data.descricoes_extras:
            for texto in iniciativa_data.descricoes_extras:
                db_extra = DescricoesExtras(
                    iniciativa_id=db_iniciativa.id,
                    descricao=texto,
                    # PLACEHOLDER DE VETOR ALTERAR DPS
                    descricao_vetor=descricao_vetor,
                )
                self.db.add(db_extra)

        self.db.commit()
        self.db.refresh(db_iniciativa)

        iniciativa = self.get_by_id(db_iniciativa.id)
        if iniciativa is None:
            raise ValueError("Erro ao recuperar iniciativa criada")
        return iniciativa

    def get_by_id(self, iniciativa_id: str) -> Optional[Iniciativa]:
        return (
            self.db.query(Iniciativa)
            .options(selectinload(Iniciativa.horarios))
            .filter(Iniciativa.id == iniciativa_id)
            .first()
        )

    def organizador_exists(self, organizador_id: str) -> bool:
        return (
            self.db.query(Organizador).filter(Organizador.id == organizador_id).first()
            is not None
        )

    def tags_exist(self, tag_ids: List[str]) -> List[str]:
        """Retorna lista de IDs de tags que existem"""
        existing_tags = self.db.query(Tag.id).filter(Tag.id.in_(tag_ids)).all()
        return [tag.id for tag in existing_tags]

    def check_duplicate_iniciativa(
        self, titulo: str, organizador_id: str, exclude_id: Optional[str] = None
    ) -> Optional[Iniciativa]:
        """Verifica se existe uma iniciativa com mesmo título e organizador"""
        query = self.db.query(Iniciativa).filter(
            and_(
                Iniciativa.titulo == titulo,
                Iniciativa.organizador_id == organizador_id,
                Iniciativa.deletado_em.is_(None),
            )
        )

        if exclude_id:
            query = query.filter(Iniciativa.id != exclude_id)

        return query.first()

    def check_conflicting_horarios(
        self,
        organizador_id: str,
        horarios: List,
        exclude_iniciativa_id: Optional[str] = None,
    ) -> List[IniciativaHorario]:
        """Verifica se há horários conflitantes com outras iniciativas do mesmo organizador"""
        conflitos = []

        for horario in horarios:
            query = (
                self.db.query(IniciativaHorario)
                .join(Iniciativa)
                .filter(
                    and_(
                        Iniciativa.organizador_id == organizador_id,
                        IniciativaHorario.data_evento == horario.data_evento,
                        Iniciativa.deletado_em.is_(None),
                        or_(
                            and_(
                                IniciativaHorario.hora_inicio <= horario.hora_inicio,
                                IniciativaHorario.hora_fim > horario.hora_inicio,
                            ),
                            and_(
                                IniciativaHorario.hora_inicio < horario.hora_fim,
                                IniciativaHorario.hora_fim >= horario.hora_fim,
                            ),
                            and_(
                                horario.hora_inicio <= IniciativaHorario.hora_inicio,
                                horario.hora_fim >= IniciativaHorario.hora_fim,
                            ),
                        ),
                    )
                )
            )

            if exclude_iniciativa_id:
                query = query.filter(Iniciativa.id != exclude_iniciativa_id)

            conflitos_horario = query.all()
            conflitos.extend(conflitos_horario)

        return conflitos

    def search_by_embedding(self, embedding: List[float], page: int, size: int):
        offset = (page - 1) * size

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        embedding_str = f"[{', '.join(str(x) for x in embedding)}]"

        query = text(
            """
            SELECT i.*, count(*) OVER() AS total_count
            FROM iniciativas i
            ORDER BY i.descricao_vetor <-> :embedding
            LIMIT :limit OFFSET :offset
        """
        )

        result = (
            self.db.execute(
                query, {"embedding": embedding_str, "limit": size, "offset": offset}
            )
            .mappings()
            .all()
        )

        if result:
            total = result[0]["total_count"]
        else:
            total = 0

        ids = [row["id"] for row in result]
        iniciativas = (
            self.db.query(Iniciativa)
            .filter(Iniciativa.id.in_(ids))
            .options(selectinload(Iniciativa.horarios))
            .all()
        )

        iniciativas_dict = {i.id: i for i in iniciativas}
        iniciativas = [iniciativas_dict[_id] for _id in ids]

        return iniciativas, total
