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
import os

from dotenv import load_dotenv
load_dotenv()

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
        size: int = 20,
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
    
    def ranking_by_rrf(
    self,
    query_text: str,
    embedding: List[float],
    page: int,
    size: int,
    min_score: float,
    rrf_k: float,
) -> Tuple[List[Iniciativa], int]:
        """
        Fusiona resultados de embedding e FTS usando RRF.
        Retorna tupla (iniciativas ordenadas, total após threshold).

        min_score e rrf_k vêm da service.
        Pesos e k específicos vêm do env.
        """

        page = max(page, 1)
        size = max(size, 1)

        weight_embedding = float(os.getenv("RRF_WEIGHT_EMBEDDING", "1.0"))
        weight_fts       = float(os.getenv("RRF_WEIGHT_FTS", "1.0"))

        k_base = max(rrf_k, 1.0)

        k_emb = float(os.getenv("RRF_K_EMBEDDING", str(k_base)))
        k_fts = float(os.getenv("RRF_K_FTS", str(k_base)))
        k_emb = max(k_emb, 1.0)
        k_fts = max(k_fts, 1.0)

        min_results = int(os.getenv("HYBRID_SEARCH_MIN_RESULTS", "1"))
        min_results = max(0, min_results)

        max_candidates_env = int(os.getenv("HYBRID_SEARCH_MAX_CANDIDATES", "200"))

        emb_items, _ = self.search_by_embedding(embedding, size=size)
        fts_items, _ = self.search_by_fts(query_text, page=1, size=size)

        if not emb_items and not fts_items:
            return [], 0

        emb_rank = {o.id: idx+1 for idx, o in enumerate(emb_items)}
        fts_rank = {o.id: idx+1 for idx, o in enumerate(fts_items)}
        all_ids = list(set(emb_rank) | set(fts_rank))

        obj_map = {o.id: o for o in emb_items}
        for o in fts_items:
            obj_map.setdefault(o.id, o)

        BIG = 1_000_000
        scored = []

        for _id in all_ids:
            r_emb = emb_rank.get(_id)
            r_fts = fts_rank.get(_id)

            score = 0.0
            if r_emb is not None:
                score += weight_embedding * (1 / (k_emb + r_emb))
            if r_fts is not None:
                score += weight_fts * (1 / (k_fts + r_fts))

            scored.append((_id, score, r_emb or BIG, r_fts or BIG))

        scored.sort(key=lambda t: (-t[1], min(t[2], t[3]), t[2], t[3]))

        if max_candidates_env > 0:
            scored = scored[:max_candidates_env]

        print(f"[RRF] threshold={min_score:.4f} | k_emb={k_emb} | k_fts={k_fts}")
        for _id, s, re, rf in scored[:20]:
            print(f"[RRF] ID={_id} | score={s:.6f} | emb={re} | fts={rf}")

        if min_score > 0:
            filtered = [t for t in scored if t[1] >= min_score]
        else:
            filtered = scored[:]

        if not filtered:
            filtered = scored[:min_results]
        elif len(filtered) < min_results:
            extra = [t for t in scored if t not in filtered]
            needed = min(min_results - len(filtered), len(extra))
            filtered.extend(extra[:needed])

        total = len(filtered)

        start = (page - 1) * size
        end = start + size
        page_slice = filtered[start:end]

        result_ids = [t[0] for t in page_slice]
        ordered = [obj_map[i] for i in result_ids]

        return ordered, total
    
    def search_by_fts(
        self, query_text: str, page: int, size: int
    ) -> Tuple[List[Iniciativa], int]:
        """
        Busca iniciativas por FTS.
        Retorna tupla (iniciativas ordenadas por relevância, total).
        """
        if self.db.bind.dialect.name != "postgresql":
            return self._search_sqlite_fallback(query_text, page, size)
        
        max_results = int(os.getenv("FTS_MAX_RESULTS", 10))

        min_rank = float(os.getenv("FTS_MIN_RANK", "0.0"))

        # Pesos para cada componente do documento
        valid_weights = {"A", "B", "C", "D"}

        def _get_weight(env_name: str, default: str) -> str:
            v = os.getenv(env_name, default).upper()
            return v if v in valid_weights else default

        title_weight = _get_weight("FTS_WEIGHT_TITLE", "A")
        desc_weight = _get_weight("FTS_WEIGHT_DESC", "B")
        tags_weight = _get_weight("FTS_WEIGHT_TAGS", "C")
        extras_weight = _get_weight("FTS_WEIGHT_EXTRAS", "B")
   
        normalized_query = (query_text or "").strip()

        if not normalized_query:
            return [], 0


        query = text(
            f"""
            WITH params AS (
                SELECT plainto_tsquery('portuguese', :query) AS ts_query
            ),
            tags_agg AS (
                SELECT
                    it.iniciativa_id,
                    string_agg(t.nome || ' ' || COALESCE(t.descricao, ''), ' ') AS tags_text
                FROM iniciativa_tag it
                JOIN tags t ON t.id = it.tag_id
                GROUP BY it.iniciativa_id
            ),
            extras_agg AS (
                SELECT
                    iniciativa_id,
                    string_agg(descricao, ' ') AS extras_text
                FROM descricoes_extras
                GROUP BY iniciativa_id
            ),
            fts_docs AS (
                SELECT
                    i.id,
                    (
                        setweight(to_tsvector('portuguese', COALESCE(i.titulo, '')), '{title_weight}')
                        || setweight(to_tsvector('portuguese', COALESCE(i.descricao, '')), '{desc_weight}')
                        || setweight(to_tsvector('portuguese', COALESCE(tags_agg.tags_text, '')), '{tags_weight}')
                        || setweight(to_tsvector('portuguese', COALESCE(extras_agg.extras_text, '')), '{extras_weight}')
                    ) AS document
                FROM iniciativas i
                LEFT JOIN tags_agg ON tags_agg.iniciativa_id = i.id
                LEFT JOIN extras_agg ON extras_agg.iniciativa_id = i.id
                WHERE i.deletado_em IS NULL
            ),
            ranked AS (
                SELECT
                    fts_docs.id,
                    ts_rank_cd(
                        fts_docs.document,
                        params.ts_query
                    ) AS rank
                FROM fts_docs
                JOIN params ON TRUE
                WHERE params.ts_query @@ fts_docs.document
            ),
            filtered AS (
                SELECT
                    id,
                    rank AS best_rank
                FROM ranked
                WHERE rank >= :min_rank
            )
            SELECT
                i.id,
                i.titulo,
                filtered.best_rank,
                COUNT(*) OVER() AS total_count
            FROM filtered
            JOIN iniciativas i ON i.id = filtered.id
            WHERE i.deletado_em IS NULL
            ORDER BY filtered.best_rank DESC, i.id
            LIMIT :limit
        """
        )

        rows = (
            self.db.execute(
                query,
                {
                    "query": normalized_query,
                    "min_rank": min_rank,
                    "limit": max_results,
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
        ordered = [m[_id] for _id in ids if _id in m]

        return ordered, total
    
    def search_by_embedding(
        self, embedding: List[float], size: int
    ) -> Tuple[List[Iniciativa], int]:
        """
        Busca iniciativas por similaridade de embedding (busca semântica).
        Retorna tupla (iniciativas ordenadas por similaridade, total).
        """

        max_results = int(os.getenv("SEMANTIC_SEARCH_MAX_RESULTS", 10))
        
        min_sim = float(os.getenv("EMBEDDING_MIN_SIM", "0.0"))
        include_main_desc_env = os.getenv("EMBEDDING_INCLUDE_MAIN_DESC", "true").lower()
        
        include_main_desc = include_main_desc_env not in ("0", "false", "no")

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        embedding_str = f"[{', '.join(str(x) for x in embedding)}]"

        all_sims_parts = []

        if include_main_desc:
            all_sims_parts.append(
                """
                SELECT
                    i.id,
                    1 - (i.descricao_vetor <-> (SELECT emb FROM q)) AS sim
                FROM iniciativas i
                WHERE i.deletado_em IS NULL
                """
            )

        all_sims_parts.append(
            """
            SELECT
                de.iniciativa_id AS id,
                1 - (de.descricao_vetor <-> (SELECT emb FROM q)) AS sim
            FROM descricoes_extras de
            JOIN iniciativas i ON i.id = de.iniciativa_id
            WHERE i.deletado_em IS NULL
            """
        )

        all_sims_sql = " UNION ALL ".join(all_sims_parts)

        query = text(
            f"""
        WITH q AS (
            SELECT (:embedding)::vector AS emb
        ),
        all_sims AS (
            {all_sims_sql}
        ),
        best AS (
            SELECT
                id,
                MAX(sim) AS best_sim
            FROM all_sims
            GROUP BY id
        ),
        filtered AS (
            SELECT
                id,
                best_sim
            FROM best
            WHERE best_sim >= :min_sim
        )
        SELECT
            i.id,
            i.titulo,
            filtered.best_sim,
            COUNT(*) OVER() AS total_count
        FROM filtered
        JOIN iniciativas i ON i.id = filtered.id
        WHERE i.deletado_em IS NULL
        ORDER BY filtered.best_sim DESC, i.id
        LIMIT :limit
        """
        )

        rows = (
            self.db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "min_sim": min_sim,
                    "limit": max_results,
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
        ordered = [m[_id] for _id in ids if _id in m]

        return ordered, total


    def _search_sqlite_fallback(
        self, query_text: str, page: int, size: int
    ) -> Tuple[List[Iniciativa], int]:
        """
        Fallback simples para ambientes sem pgvector/FTS (SQLite em testes).
        Usa apenas filtros LIKE para título/descrição.
        """
        pattern = f"%{query_text}%" if query_text else None
        base_query = (
            self.db.query(Iniciativa)
            .filter(Iniciativa.deletado_em.is_(None))
            .options(
                selectinload(Iniciativa.horarios),
            )
        )
        if pattern:
            base_query = base_query.filter(
                or_(
                    Iniciativa.titulo.ilike(pattern),
                    Iniciativa.descricao.ilike(pattern),
                )
            )

        total = base_query.count()
        iniciativas = (
            base_query.order_by(Iniciativa.criado_em.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return iniciativas, total

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

    def search_hibrida(
        self,
        query_text: str,
        embedding: List[float],
        page: int,
        size: int,
        min_score: float,
        rrf_k: float,
    ) -> Tuple[List[Iniciativa], int]:
        
        if self.db.bind.dialect.name != "postgresql":
            return self._search_sqlite_fallback(query_text, page, size)

        offset = (page - 1) * size

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        embedding_str = f"[{', '.join(str(x) for x in embedding)}]"
        normalized_query = (query_text or "").strip()
        rrf_constant = max(rrf_k, 1.0)

        query = text(
            """
            WITH params AS (
                SELECT
                    (:embedding)::vector AS emb,
                    NULLIF(:fts_query, '') AS raw_query,
                    CASE
                        WHEN NULLIF(:fts_query, '') IS NULL
                            THEN NULL
                        ELSE plainto_tsquery('portuguese', :fts_query)
                    END AS ts_query
            ),
            semantic_candidates AS (
                SELECT i.id, 1 - (i.descricao_vetor <-> (SELECT emb FROM params)) AS sim
                FROM iniciativas i
                WHERE i.deletado_em IS NULL
                UNION ALL
                SELECT de.iniciativa_id AS id, 1 - (de.descricao_vetor <-> (SELECT emb FROM params)) AS sim
                FROM descricoes_extras de
                JOIN iniciativas i ON i.id = de.iniciativa_id
                WHERE i.deletado_em IS NULL
            ),
            semantic_best AS (
                SELECT
                    id,
                    MAX(sim) AS best_sim
                FROM semantic_candidates
                GROUP BY id
            ),
            semantic_ranked AS (
                SELECT
                    id,
                    best_sim,
                    ROW_NUMBER() OVER (ORDER BY best_sim DESC, id) AS sem_rank
                FROM semantic_best
            ),
            tags_agg AS (
                SELECT
                    it.iniciativa_id,
                    string_agg(t.nome || ' ' || COALESCE(t.descricao, ''), ' ') AS tags_text
                FROM iniciativa_tag it
                JOIN tags t ON t.id = it.tag_id
                GROUP BY it.iniciativa_id
            ),
            extras_agg AS (
                SELECT
                    iniciativa_id,
                    string_agg(descricao, ' ') AS extras_text
                FROM descricoes_extras
                GROUP BY iniciativa_id
            ),
            fts_docs AS (
                SELECT
                    i.id,
                    (
                        setweight(to_tsvector('portuguese', COALESCE(i.titulo, '')), 'A')
                        || setweight(to_tsvector('portuguese', COALESCE(i.descricao, '')), 'B')
                        || setweight(to_tsvector('portuguese', COALESCE(tags_agg.tags_text, '')), 'C')
                        || setweight(to_tsvector('portuguese', COALESCE(extras_agg.extras_text, '')), 'C')
                    ) AS document
                FROM iniciativas i
                LEFT JOIN tags_agg ON tags_agg.iniciativa_id = i.id
                LEFT JOIN extras_agg ON extras_agg.iniciativa_id = i.id
                WHERE i.deletado_em IS NULL
            ),
            fts_ranked AS (
                SELECT
                    fts_docs.id,
                    ts_rank_cd(fts_docs.document, params.ts_query) AS fts_score,
                    ROW_NUMBER() OVER (
                        ORDER BY ts_rank_cd(fts_docs.document, params.ts_query) DESC, fts_docs.id
                    ) AS fts_rank
                FROM fts_docs
                JOIN params ON TRUE
                WHERE params.ts_query IS NOT NULL
                  AND params.ts_query @@ fts_docs.document
            ),
            combined AS (
                SELECT
                    i.id,
                    sem.best_sim,
                    sem.sem_rank,
                    fts.fts_rank,
                    (
                        COALESCE(1.0 / (:rrf_k + sem.sem_rank), 0)
                        + COALESCE(1.0 / (:rrf_k + fts.fts_rank), 0)
                    ) AS rrf_score
                FROM iniciativas i
                LEFT JOIN semantic_ranked sem ON sem.id = i.id
                LEFT JOIN fts_ranked fts ON fts.id = i.id
                WHERE i.deletado_em IS NULL
                  AND (sem.id IS NOT NULL OR fts.id IS NOT NULL)
            )
            SELECT
                combined.id,
                combined.rrf_score,
                combined.best_sim,
                COUNT(*) OVER() AS total_count
            FROM combined
            ORDER BY combined.rrf_score DESC, combined.best_sim DESC, combined.id
            LIMIT :limit OFFSET :offset
        """
        )

        rows = (
            self.db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "fts_query": normalized_query,
                    "limit": size,
                    "offset": offset,
                    "rrf_k": rrf_constant,
                },
            )
            .mappings()
            .all()
        )

        if not rows:
            return [], 0

        filtered_rows = [r for r in rows if (r.get("rrf_score") or 0.0) >= min_score]

        if not filtered_rows and rows:
            filtered_rows = [rows[0]]

        ids = [r["id"] for r in filtered_rows]
        iniciativas = (
            self.db.query(Iniciativa)
            .filter(
                Iniciativa.id.in_(ids),
                Iniciativa.deletado_em.is_(None),
            )
            .options(selectinload(Iniciativa.horarios))
            .all()
        )
        m = {i.id: i for i in iniciativas}
        ordered = [m[_id] for _id in ids if _id in m]

        return ordered, len(filtered_rows)

def _get_rrf_base_k(self) -> int:
    # K base global do RRF (mínimo 60 por segurança)
    return max(int(os.getenv("RRF_K", "60")), 60)

def _get_rrf_k_emb(self) -> int:
    base = self._get_rrf_base_k()
    return max(int(os.getenv("RRF_K_EMBEDDING", str(base))), 60)

def _get_rrf_k_fts(self) -> int:
    base = self._get_rrf_base_k()
    return max(int(os.getenv("RRF_K_FTS", str(base))), 60)

def _get_rrf_weights(self) -> Tuple[float, float]:
    weight_embedding = float(os.getenv("RRF_WEIGHT_EMBEDDING", "1.0"))
    weight_fts = float(os.getenv("RRF_WEIGHT_FTS", "1.0"))
    return weight_embedding, weight_fts

def _get_rrf_candidate_multiplier(self) -> int:
    # ex.: quantas vezes o tamanho da página você quer buscar para RRF
    return max(int(os.getenv("RRF_CAND_MULTIPLIER", "5")), 1)

def _get_default_min_score(self) -> float:
    # min_score global para híbrida (pode deixar baixo e ajustar depois)
    return float(os.getenv("RRF_MIN_SCORE", "0.0"))
