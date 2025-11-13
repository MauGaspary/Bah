import os

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

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
from app.utils.exceptions import ResourceNotFound


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
        """Cria uma nova iniciativa com embeddings."""
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

    def get_by_id(
        self, iniciativa_id: str, allow_deleted: bool = False
    ) -> Optional[Iniciativa]:
        """
        Busca uma iniciativa pelo ID.
        Por padrão, retorna apenas iniciativas não deletadas.
        """
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
        """
        Busca uma iniciativa ativa (não deletada) pelo ID.
        Lança ResourceNotFound se não encontrar.
        """
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
        """Lista iniciativas com filtros e paginação (usado pelo admin)."""
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

    def count_iniciativas(
        self,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
    ) -> int:
        """Conta iniciativas com filtros (usado pelo admin para paginação)."""
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
        Aplica alterações parciais na Iniciativa (PATCH).
        - Campos simples: atualiza somente os presentes em `data`.
        - tags_ids: substitui o conjunto de tags.
        - horarios: substitui a lista de horários (se fornecida).
        - descricoes_extras: suporta add, update, delete
        - Lança ResourceNotFound se não existir ou estiver soft-deletada.
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
            self.db.query(IniciativaHorario).filter(
                IniciativaHorario.iniciativa_id == obj.id
            ).delete(synchronize_session=False)
            self.db.flush()

            for h in data["horarios"]:
                self.db.add(
                    IniciativaHorario(
                        iniciativa_id=obj.id,
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

    def soft_delete(self, iniciativa_id: str, deletado_por: str) -> bool:
        """
        Soft delete de iniciativa.
        Retorna True se deletou ou já estava deletada, False se não existir.
        """
        iniciativa = self.get_by_id(iniciativa_id, allow_deleted=True)
        if not iniciativa:
            return False

        if iniciativa.deletado_em is None:
            iniciativa.deletado_em = func.now()
            iniciativa.deletado_por = deletado_por
            self.db.commit()
            self.db.refresh(iniciativa)

        return True

    def organizador_exists(self, organizador_id: str) -> bool:
        """Verifica se organizador existe."""
        return (
            self.db.query(Organizador).filter(Organizador.id == organizador_id).first()
            is not None
        )

    def tags_exist(self, tag_ids: List[str]) -> List[str]:
        """Retorna lista de IDs de tags que existem."""
        existing_tags = self.db.query(Tag.id).filter(Tag.id.in_(tag_ids)).all()
        return [tag.id for tag in existing_tags]

    def check_duplicate_iniciativa(
        self, titulo: str, organizador_id: str, exclude_id: Optional[str] = None
    ) -> Optional[Iniciativa]:
        """Verifica se existe uma iniciativa com mesmo título e organizador."""
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
        """Verifica se há horários conflitantes com outras iniciativas do mesmo organizador."""
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
        Retorna todos os horários de iniciativas para um determinado mês.
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
        Carrega tags em lote para iniciativas do calendário.
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
        """Retorna o último dia do mês."""
        import calendar

        last_day_num = calendar.monthrange(data.year, data.month)[1]
        return data.replace(day=last_day_num)

    def search_by_embedding(
        self, embedding: List[float], page: int, size: int
    ) -> Tuple[List[Iniciativa], int]:
        """
        Busca iniciativas por similaridade de embedding (busca semântica).
        Retorna tupla (iniciativas ordenadas por similaridade, total).
        """
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
                WHERE i.deletado_em IS NULL
                UNION ALL
                SELECT de.iniciativa_id AS id, 1 - (de.descricao_vetor <-> (SELECT emb FROM q)) AS sim
                FROM descricoes_extras de
                JOIN iniciativas i ON i.id = de.iniciativa_id
                WHERE i.deletado_em IS NULL
            ),
            best AS (
                SELECT id, MAX(sim) AS best_sim
                FROM all_sims
                GROUP BY id
            )
            SELECT i.id, i.titulo, best.best_sim, COUNT(*) OVER() AS total_count
            FROM best
            JOIN iniciativas i ON i.id = best.id
            WHERE i.deletado_em IS NULL
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

        for r in rows:
            sim = r["best_sim"] or 0.0
            print(f"[SIM] ID={r['id']} | sim={sim:.4f} | título={r.get('titulo','')}")

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

    def ranking_by_rrf(
        self,
        embedding: List[float],
        query_text: str,
        page: int,
        size: int,
        *,
        k: int = 60,
    ) -> Tuple[List[Iniciativa], int]:
        """
        Fusiona resultados de embedding e FTS usando RRF.
        Retorna tupla (iniciativas ordenadas, total).
        """

        weight_embedding = float(os.getenv("RRF_WEIGHT_EMBEDDING", "1.0"))
        weight_fts = float(os.getenv("RRF_WEIGHT_FTS", "1.0"))
        k_default = int(os.getenv("RRF_K", str(k)))
        k_emb = int(os.getenv("RRF_K_EMBEDDING", str(k_default)))
        k_fts = int(os.getenv("RRF_K_FTS", str(k_default)))

        emb_items, emb_total = self.search_by_embedding(embedding, page=page, size=size)
        fts_items, _fts_total = self.search_by_fts(query_text, page=page, size=size)

        emb_rank = {obj.id: idx + 1 for idx, obj in enumerate(emb_items)}
        fts_rank = {obj.id: idx + 1 for idx, obj in enumerate(fts_items)}
        all_ids = list(set(emb_rank.keys()) | set(fts_rank.keys()))

        obj_by_id: Dict[str, Iniciativa] = {}
        for o in emb_items:
            obj_by_id[o.id] = o
        for o in fts_items:
            obj_by_id.setdefault(o.id, o)

        scored: List[Tuple[str, float, int, int]] = []
        for _id in all_ids:
            r_emb = emb_rank.get(_id)
            r_fts = fts_rank.get(_id)
            score = 0.0
            if r_emb is not None:
                score += weight_embedding * (1.0 / (k_emb + r_emb))
            if r_fts is not None:
                score += weight_fts * (1.0 / (k_fts + r_fts))
            scored.append((_id, score, r_emb or 1_000_000, r_fts or 1_000_000))

        scored.sort(key=lambda t: (-t[1], min(t[2], t[3]), t[2], t[3]))
        fused_ids = [t[0] for t in scored[:size]]
        ordered = [obj_by_id[i] for i in fused_ids if i in obj_by_id]
        total = emb_total
        return ordered, total
    
    def search_by_fts(
        self, query_text: str, page: int, size: int
    ) -> Tuple[List[Iniciativa], int]:
        """
        Busca iniciativas por FTS.
        Retorna tupla (iniciativas ordenadas por relevância, total).
        """
        offset = (page - 1) * size

        query = text(
            """
            WITH all_texts AS (
                -- Texto principal das iniciativas
                SELECT
                    i.id,
                    to_tsvector('portuguese', coalesce(i.titulo, '') || ' ' || coalesce(i.descricao, '')) AS document
                FROM iniciativas i
                WHERE i.deletado_em IS NULL

                UNION ALL

                -- Textos adicionais das descricoes_extras
                SELECT
                    de.iniciativa_id AS id,
                    to_tsvector('portuguese', coalesce(de.descricao, '')) AS document
                FROM descricoes_extras de
                JOIN iniciativas i ON i.id = de.iniciativa_id
                WHERE i.deletado_em IS NULL
            ),
            ranked AS (
                SELECT
                    id,
                    MAX(ts_rank_cd(document, plainto_tsquery('portuguese', :query))) AS rank
                FROM all_texts
                WHERE document @@ plainto_tsquery('portuguese', :query)
                GROUP BY id
            )
            SELECT
                i.id,
                i.titulo,
                ranked.rank AS best_rank,
                COUNT(*) OVER() AS total_count
            FROM ranked
            JOIN iniciativas i ON i.id = ranked.id
            WHERE i.deletado_em IS NULL
            ORDER BY ranked.rank DESC
            LIMIT :limit OFFSET :offset
            """
        )

        rows = (
            self.db.execute(
                query,
                {
                    "query": query_text,
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

        for r in rows:
            rank = r["best_rank"] or 0.0
            print(f"[FTS] ID={r['id']} | rank={rank:.4f} | título={r.get('titulo','')}")

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
