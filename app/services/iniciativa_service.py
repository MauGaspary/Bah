import math
import os
from datetime import date, datetime
from typing import Any, Dict, List, Mapping, Optional, Sequence

from fastapi import HTTPException
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.models.iniciativa_horario_model import HorarioTipo
from app.models.usuario_model import Usuario
from app.repositories.iniciativa_repository import IniciativaRepository
from app.schemas.iniciativa_schema import (
    CalendarioHorarioTipo,
    CalendarioIniciativaItem,
    CalendarioMensalResponse,
    DiaCalendario,
    IniciativaCreate,
    IniciativaFiltersSchema,
    IniciativaListResponse,
    IniciativaListResponseSchema,
    IniciativaPatchSchema,
    IniciativaResponse,
    IniciativaSchema,
    TagSchema,
)

from dotenv import load_dotenv
load_dotenv()
class IniciativaService:

    def __init__(self, db: Session, model: Optional[SentenceTransformer] = None):
        self.repository = IniciativaRepository(db)
        self.model = model

    def listar_iniciativas(
        self,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        order_by: str = "criado_em",
        order_dir: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> IniciativaListResponseSchema:
        if created_from and created_to and created_from > created_to:
            raise ValueError("Data inicial deve ser menor que data final")

        valid_order_fields = ["criado_em", "titulo", "destaque", "editado_em"]
        if order_by not in valid_order_fields:
            order_by = "criado_em"

        iniciativas_models = self.repository.list_iniciativas(
            q, created_from, created_to, order_by, order_dir, page, size
        )
        iniciativas = [
            IniciativaSchema.model_validate(iniciativa)
            for iniciativa in iniciativas_models
        ]

        total = self.repository.count_iniciativas(q, created_from, created_to)

        filters = IniciativaFiltersSchema(
            q=q,
            created_from=created_from,
            created_to=created_to,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

        return IniciativaListResponseSchema(
            items=iniciativas, total=total, filters=filters
        )

    def delete_iniciativa(self, iniciativa_id: str, deletado_por: str) -> None:
        """Soft delete de iniciativa (usado pelo admin)."""
        exists = self.repository.soft_delete(iniciativa_id, deletado_por)
        if not exists:
            raise ValueError("Iniciativa não encontrada")

    def get_iniciativa_by_id_admin(self, iniciativa_id: str) -> IniciativaSchema:
        """Busca uma iniciativa ativa (não deletada) pelo ID e retorna o schema admin completo."""
        iniciativa = self.repository.get_by_id(iniciativa_id, allow_deleted=False)
        if not iniciativa:
            raise ValueError("Iniciativa não encontrada")
        return IniciativaSchema.model_validate(iniciativa)

    def patch_iniciativa(
        self,
        iniciativa_id: str,
        payload: IniciativaPatchSchema,
        editado_por: Optional[str] = None,
        model: Optional[SentenceTransformer] = None,
    ) -> IniciativaSchema:
        """
        Aplica alterações parciais na iniciativa e retorna o objeto completo atualizado.
        Regras 404/422 já são garantidas pelo repo e pelos validadores do schema.
        """
        data: Dict[str, Any] = payload.model_dump(exclude_none=True)

        if "descricoes_extras_update" in data and data["descricoes_extras_update"]:
            if model is None:
                raise ValueError(
                    "Modelo de embedding não disponível para atualizar descrições extras"
                )

            descricoes_atualizadas = []
            for item in data["descricoes_extras_update"]:
                texto: str = item.get("descricao")
                if not texto:
                    descricoes_atualizadas.append(item)
                    continue

                vetor = model.encode(
                    texto, convert_to_numpy=True, normalize_embeddings=True
                )
                novo_item = dict(item)
                novo_item["descricao_vetor"] = vetor
                descricoes_atualizadas.append(novo_item)

            data["descricoes_extras_update"] = descricoes_atualizadas

        if "descricoes_extras_add" in data and data["descricoes_extras_add"]:
            if model is None:
                raise ValueError(
                    "Modelo de embedding não disponível para adicionar descrições extras"
                )
            textos = data["descricoes_extras_add"]
            extras_novos = []
            for texto in textos:
                vetor = model.encode(
                    texto, convert_to_numpy=True, normalize_embeddings=True
                )
                extras_novos.append({"descricao": texto, "descricao_vetor": vetor})
            data["descricoes_extras_add"] = extras_novos

        updated = self.repository.update_partial(
            iniciativa_id=iniciativa_id,
            data=data,
            editado_por=editado_por,
            model=model,
        )
        return IniciativaSchema.model_validate(updated)

    def _convert_horario_tipo(self, tipo: HorarioTipo) -> CalendarioHorarioTipo:
        """Converte o enum do model para o enum do schema de calendário."""
        mapping = {
            HorarioTipo.PRESENCIAL: CalendarioHorarioTipo.PRESENCIAL,
            HorarioTipo.ONLINE: CalendarioHorarioTipo.ONLINE,
            HorarioTipo.HIBRIDO: CalendarioHorarioTipo.HIBRIDO,
        }
        return mapping[tipo]

    def create_iniciativa(
        self, iniciativa_data: IniciativaCreate, criado_por: str
    ) -> IniciativaResponse:
        """Cria uma nova iniciativa (com embeddings)."""
        if criado_por != "sistema":
            usuario_existe = (
                self.repository.db.query(Usuario)
                .filter(Usuario.id == criado_por)
                .first()
            )
            if not usuario_existe:
                raise ValueError("Usuário criador não encontrado")

        if iniciativa_data.organizador_id:
            if not self.repository.organizador_exists(iniciativa_data.organizador_id):
                raise ValueError(
                    f"Organizador não encontrado com ID: {iniciativa_data.organizador_id}"
                )
        else:
            raise ValueError("organizador_id é obrigatório")

        if iniciativa_data.tag_ids:
            existing_tags = self.repository.tags_exist(iniciativa_data.tag_ids)
            missing_tags = set(iniciativa_data.tag_ids) - set(existing_tags)
            if missing_tags:
                raise ValueError(f"Tags não encontradas: {', '.join(missing_tags)}")

        if iniciativa_data.organizador_id:
            duplicate = self.repository.check_duplicate_iniciativa(
                iniciativa_data.titulo, iniciativa_data.organizador_id
            )
            if duplicate:
                raise ValueError(
                    "Já existe uma iniciativa com este título para este organizador"
                )

        if iniciativa_data.organizador_id:
            conflicting_horarios = self.repository.check_conflicting_horarios(
                iniciativa_data.organizador_id, iniciativa_data.horarios
            )
            if conflicting_horarios:
                pass

        try:
            print("model", self.model)
            if self.model is None:
                raise RuntimeError("Modelo de embedding não disponível")

            embedding = self.model.encode(  # type: ignore
                iniciativa_data.descricao.lower(),
                convert_to_numpy=True,
                normalize_embeddings=True,
            )

            embeddings_descricoes_extras = []
            for description_for_search in iniciativa_data.descricoes_extras or []:
                embedding_extra = self.model.encode(
                    description_for_search.lower(),
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                embeddings_descricoes_extras.append(embedding_extra)

            iniciativa = self.repository.create(
                iniciativa_data,
                criado_por,
                descricao_vetor=embedding,
                descricoes_extras_vetores=embeddings_descricoes_extras,
            )

            return IniciativaResponse.model_validate(iniciativa)

        except Exception as e:
            print(f"Erro na criação: {type(e).__name__}: {str(e)}")

            if "check constraint" in str(e).lower() or "constraint" in str(e).lower():
                raise ValueError(
                    "Dados inválidos: verifique se a hora de fim é maior que a hora de início"
                ) from e
            raise RuntimeError(f"Erro interno do servidor: {str(e)}") from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        """Busca uma iniciativa pelo ID (endpoint público)."""
        iniciativa = self.repository.get_by_id(iniciativa_id)
        if not iniciativa:
            raise HTTPException(status_code=404, detail="Iniciativa não encontrada")
        return IniciativaResponse.model_validate(iniciativa)

    def get_calendario_mensal(self, data: date) -> CalendarioMensalResponse:
        """Retorna o calendário de iniciativas para o mês especificado (endpoint público)."""
        try:
            rows = self.repository.get_horarios_do_mes(data)
            tags_by_iniciativa = self.repository.get_tags_por_iniciativa(rows)
            return self.build_calendario_response(data, rows, tags_by_iniciativa)

        except Exception as e:
            print(f"Erro no calendário: {type(e).__name__}: {str(e)}")
            raise e

    def build_month_days(self, ref: date) -> List[date]:
        """Retorna todos os dias do mes de ref, ordenados."""
        import calendar
        from datetime import timedelta

        first_day = ref.replace(day=1)

        last_day_num = calendar.monthrange(ref.year, ref.month)[1]
        last_day = ref.replace(day=last_day_num)

        days = []
        current = first_day
        while current <= last_day:
            days.append(current)
            current = current + timedelta(days=1)

        return days

    def group_horarios_by_day(
        self, rows: Sequence, tags_by_iniciativa: Mapping[str, List[TagSchema]]
    ) -> Dict[date, List[CalendarioIniciativaItem]]:
        """
        Constrói itens (um por horário) e agrupa por data_evento.
        Ordena dentro do dia por (hora_inicio ASC, titulo ASC).
        Preenche tags a partir de tags_by_iniciativa.
        """
        grouped: Dict[date, List[CalendarioIniciativaItem]] = {}

        for row in rows:
            item = CalendarioIniciativaItem(
                iniciativa_id=row.iniciativa_id,
                horario_id=row.horario_id,
                titulo=row.titulo,
                descricao=row.descricao,
                hora_inicio=row.hora_inicio,
                hora_fim=row.hora_fim,
                tipo=self._convert_horario_tipo(row.tipo),
                link=row.link,
                local=row.local,
                imagem_url=row.imagem_url,
                destaque=row.destaque,
                tags=tags_by_iniciativa.get(row.iniciativa_id, []),
            )

            data_evento = row.data_evento
            if data_evento not in grouped:
                grouped[data_evento] = []
            grouped[data_evento].append(item)

        for data_evento in grouped:
            grouped[data_evento].sort(key=lambda x: (x.hora_inicio, x.titulo))

        return grouped

    def build_calendario_response(
        self,
        ref: date,
        rows: Sequence,
        tags_by_iniciativa: Mapping[str, List[TagSchema]],
    ) -> CalendarioMensalResponse:
        """
        Gera um esqueleto (todos os dias), agrupa itens e
        retorna o DTO final com mes="YYYY-MM" e lista de DiaCalendario.
        """
        month_days = self.build_month_days(ref)

        grouped_horarios = self.group_horarios_by_day(rows, tags_by_iniciativa)

        dias = []
        for day in month_days:
            iniciativas = grouped_horarios.get(day, [])
            dias.append(DiaCalendario(data=day, iniciativas=iniciativas))

        return CalendarioMensalResponse(
            mes=f"{ref.year:04d}-{ref.month:02d}", dias=dias
        )

    def search_iniciativas(
        self, query: str, page: int, size: int
    ) -> IniciativaListResponse:
        """Busca híbrida de iniciativas combinando embedding e sinais lexicais."""
        if self.model is None:
            raise ValueError("Modelo de embedding não disponível")

        try:
            min_score = float(os.getenv("HYBRID_SEARCH_MIN_SCORE", "0.0"))
        except ValueError:
            min_score = 0.0

        try:
            max_results_env = int(os.getenv("HYBRID_SEARCH_MAX_RESULTS", "50"))
        except ValueError:
            max_results_env = 50

        max_results = max(1, max_results_env)
        size = max(1, min(size, max_results))
        max_pages = max(1, math.ceil(max_results / size))
        if page > max_pages:
            page = max_pages

        embedding = self.model.encode(
            query.lower(), convert_to_numpy=True, normalize_embeddings=True
        )

        try:
            rrf_k_env = float(os.getenv("HYBRID_SEARCH_RRF_K", "60"))
        except ValueError:
            rrf_k_env = 60.0
        rrf_k = max(rrf_k_env, 1.0)

        try:
            iniciativas, total = self.repository.ranking_by_rrf(
                query, embedding, page, size, min_score, rrf_k
            )

            items = [IniciativaResponse.model_validate(i) for i in iniciativas]

            filters = IniciativaFiltersSchema(q=query, page=page, size=size)
            return IniciativaListResponse(items=items, total=total, filters=filters)
        except Exception as e:
            print(f"Erro na busca: {type(e).__name__}: {str(e)}")
            raise ValueError(f"Erro interno do servidor na service: {str(e)}") from e
