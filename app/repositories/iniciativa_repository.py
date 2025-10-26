from datetime import date
from typing import Dict, List, Optional

import numpy as np
from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.orm import Session, selectinload

from app.models.descricoes_extras_model import DescricoesExtras
from app.models.iniciativa_horario_model import IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.iniciativa_tag_model import IniciativaTag
from app.models.organizador_model import Organizador
from app.models.tag_model import Tag
from app.schemas.iniciativa_schema import IniciativaCreate, TagSchema


class IniciativaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        iniciativa_data: IniciativaCreate,
        criado_por: str,
        descricao_vetor: List[float],
        descricoes_extras_vetores: List[List[float]],
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

        if iniciativa_data.descricoes_extras:
            for texto, embedding_extra in zip(
                iniciativa_data.descricoes_extras, descricoes_extras_vetores
            ):
                db_extra = DescricoesExtras(
                    iniciativa_id=db_iniciativa.id,
                    descricao=texto,
                    descricao_vetor=embedding_extra,
                )
                self.db.add(db_extra)

        if iniciativa_data.tag_ids:
            for tag_id in iniciativa_data.tag_ids:
                db_iniciativa_tag = IniciativaTag(
                    iniciativa_id=db_iniciativa.id, tag_id=tag_id
                )
                self.db.add(db_iniciativa_tag)

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

    def get_horarios_do_mes(self, data: date) -> List:
        """
        Query principal:
        FROM iniciativa_horarios h JOIN iniciativas i ON i.id = h.iniciativa_id
        WHERE h.data_evento BETWEEN :first_day AND :last_day AND i.deletado_em IS NULL
        ORDER BY h.data_evento ASC, h.hora_inicio ASC, i.titulo ASC
        """

        first_day = data.replace(day=1)
        last_day = self._get_last_day_of_month(data)

        query = (
            select(
                Iniciativa.id.label("iniciativa_id"),
                Iniciativa.titulo,
                Iniciativa.descricao,
                Iniciativa.link,
                Iniciativa.local,
                Iniciativa.imagem_url,
                Iniciativa.destaque,
                IniciativaHorario.id.label("horario_id"),
                IniciativaHorario.data_evento,
                IniciativaHorario.hora_inicio,
                IniciativaHorario.hora_fim,
                IniciativaHorario.tipo,
            )
            .select_from(
                IniciativaHorario.__table__.join(
                    Iniciativa.__table__,
                    Iniciativa.id == IniciativaHorario.iniciativa_id,
                )
            )
            .where(
                and_(
                    IniciativaHorario.data_evento.between(first_day, last_day),
                    Iniciativa.deletado_em.is_(None),
                )
            )
            .order_by(
                IniciativaHorario.data_evento.asc(),
                IniciativaHorario.hora_inicio.asc(),
                Iniciativa.titulo.asc(),
            )
        )

        result = self.db.execute(query)
        return result.fetchall()

    def get_tags_por_iniciativa(self, rows: List) -> Dict[str, List[TagSchema]]:
        """
        Carrega tags em lote:
        Pega a lista de iniciativa_id retornados na query acima.
        Busca uma vez:
        SELECT it.iniciativa_id, t.id, t.nome, t.descricao
        FROM iniciativa_tags it
        JOIN tags t ON t.id = it.tag_id
        WHERE it.iniciativa_id IN (:ids)
        ORDER BY t.nome ASC;
        """
        if not rows:
            return {}

        iniciativa_ids = [row.iniciativa_id for row in rows]

        query = (
            select(IniciativaTag.iniciativa_id, Tag.id, Tag.nome, Tag.descricao)
            .select_from(
                IniciativaTag.__table__.join(
                    Tag.__table__, Tag.id == IniciativaTag.tag_id
                )
            )
            .where(IniciativaTag.iniciativa_id.in_(iniciativa_ids))
            .order_by(Tag.nome.asc())
        )

        result = self.db.execute(query)
        rows_tags = result.fetchall()

        tags_by_iniciativa: Dict[str, List[TagSchema]] = {}
        for row in rows_tags:
            iniciativa_id = row.iniciativa_id
            if iniciativa_id not in tags_by_iniciativa:
                tags_by_iniciativa[iniciativa_id] = []

            tag = TagSchema(id=row.id, nome=row.nome, descricao=row.descricao)
            tags_by_iniciativa[iniciativa_id].append(tag)

        return tags_by_iniciativa

    def _get_last_day_of_month(self, data: date) -> date:
        """Retorna o último dia do mês"""
        import calendar

        last_day_num = calendar.monthrange(data.year, data.month)[1]
        return data.replace(day=last_day_num)

    def create_index_if_not_exists(self):
        """
        Criar índice se não existir: iniciativa_horarios (data_evento, hora_inicio)
        Confirmar iniciativas.deletado_em (soft delete) já existe
        """

        index_name = "idx_iniciativa_horarios_data_hora"

        check_index_query = """
        SELECT EXISTS (
            SELECT 1 FROM pg_indexes
            WHERE indexname = :index_name
        )
        """

        result = self.db.execute(
            select(func.text(check_index_query)).params(index_name=index_name)
        )

        if not result.scalar():
            create_index_query = """
            CREATE INDEX idx_iniciativa_horarios_data_hora
            ON iniciativa_horarios (data_evento, hora_inicio)
            """
            self.db.execute(create_index_query)
            self.db.commit()

    def search_by_embedding(self, embedding: List[float], page: int, size: int):
        offset = (page - 1) * size

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        embedding_str = f"[{', '.join(str(x) for x in embedding)}]"

        query = text(
            """
            WITH q AS (
                SELECT (:embedding)::vector AS emb
            ),
            all_sims AS (
                SELECT i.id, 1 - (i.descricao_vetor <-> (SELECT emb FROM q)) AS sim
                FROM iniciativas i
                UNION ALL
                SELECT de.iniciativa_id AS id, 1 - (de.descricao_vetor <-> (SELECT emb FROM q)) AS sim
                FROM descricoes_extras de
            ),
            best AS (
                SELECT id, MAX(sim) AS best_sim
                FROM all_sims
                GROUP BY id
            )
            SELECT i.id, i.titulo, best.best_sim, COUNT(*) OVER() AS total_count
            FROM best
            JOIN iniciativas i ON i.id = best.id
            ORDER BY best.best_sim DESC
            LIMIT :limit OFFSET :offset
        """
        )

        rows = (
            self.db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "limit": size,
                    "offset": offset,
                },
            )
            .mappings()
            .all()
        )

        total = rows[0]["total_count"] if rows else 0
        if not rows:
            return [], 0

        # imprime similaridade (somente logs)
        for r in rows:
            sim = r["best_sim"] or 0.0
            print(f"[SIM] ID={r['id']} | sim={sim:.4f} | título={r.get('titulo','')}")

        # agora buscamos as entidades e preservamos a ordem do ranking
        ids = [r["id"] for r in rows]
        iniciativas = (
            self.db.query(Iniciativa)
            .filter(Iniciativa.id.in_(ids))
            .options(selectinload(Iniciativa.horarios))
            .all()
        )
        m = {i.id: i for i in iniciativas}
        ordered = [m[_id] for _id in ids]

        return ordered, total
