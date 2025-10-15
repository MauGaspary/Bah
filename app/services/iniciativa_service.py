from typing import List, Dict, Mapping, Sequence

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date, time

from app.models.usuario_model import Usuario
from app.repositories.iniciativa_repository import IniciativaRepository
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse, CalendarioMensalResponse, CalendarioIniciativaItem, DiaCalendario, TagSchema


class IniciativaService:
    def __init__(self, db: Session):
        self.repository = IniciativaRepository(db)

    def create_iniciativa(
        self, iniciativa_data: IniciativaCreate, criado_por: str
    ) -> IniciativaResponse:
        if criado_por != "sistema":
            usuario_existe = (
                self.repository.db.query(Usuario)
                .filter(Usuario.id == criado_por)
                .first()
            )
            if not usuario_existe:
                raise HTTPException(
                    status_code=422, detail="Usuário criador não encontrado"
                )

        if iniciativa_data.organizador_id:
            if not self.repository.organizador_exists(iniciativa_data.organizador_id):
                raise HTTPException(
                    status_code=422,
                    detail=f"Organizador não encontrado com ID: {iniciativa_data.organizador_id}",
                )
        else:
            raise HTTPException(status_code=422, detail="organizador_id é obrigatório")

        if iniciativa_data.tag_ids:
            existing_tags = self.repository.tags_exist(iniciativa_data.tag_ids)
            missing_tags = set(iniciativa_data.tag_ids) - set(existing_tags)
            if missing_tags:
                raise HTTPException(
                    status_code=422,
                    detail=f"Tags não encontradas: {', '.join(missing_tags)}",
                )

        if iniciativa_data.organizador_id:
            duplicate = self.repository.check_duplicate_iniciativa(
                iniciativa_data.titulo, iniciativa_data.organizador_id
            )
            if duplicate:
                raise HTTPException(
                    status_code=422,
                    detail="Já existe uma iniciativa com este título para este organizador",
                )

        if iniciativa_data.organizador_id:
            conflicting_horarios = self.repository.check_conflicting_horarios(
                iniciativa_data.organizador_id, iniciativa_data.horarios
            )
            if conflicting_horarios:

                pass

        try:
            iniciativa = self.repository.create(iniciativa_data, criado_por)
            return IniciativaResponse.model_validate(iniciativa)
        except Exception as e:
            print(f"Erro na criação: {type(e).__name__}: {str(e)}")

            if "check constraint" in str(e).lower() or "constraint" in str(e).lower():
                raise HTTPException(
                    status_code=422,
                    detail="Dados inválidos: verifique se a hora de fim é maior que a hora de início",
                ) from e
            raise HTTPException(
                status_code=500, detail=f"Erro interno do servidor: {str(e)}"
            ) from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        iniciativa = self.repository.get_by_id(iniciativa_id)
        if not iniciativa:
            raise HTTPException(status_code=404, detail="Iniciativa não encontrada")
        return IniciativaResponse.model_validate(iniciativa)

    def get_calendario_mensal(self, data: date) -> CalendarioMensalResponse:
        """Retorna o calendário de iniciativas para o mês especificado"""
        try:
            rows = self.repository.get_calendario_mensal(data)
            tags_by_iniciativa = self.repository.get_tags_by_iniciativa(rows)
            return self.build_calendario_mensal(data, rows, tags_by_iniciativa)

        except Exception as e:
            print(f"Erro no calendário: {type(e).__name__}: {str(e)}")
            raise e

    def build_month_days(self, ref: date) -> List[date]:
        """Retorna todos os dias do mes de ref, ordenados"""
        import calendar

        first_day = ref.replace(day=1)

        last_day_num = calendar.monthrange(ref.year, ref.month)[1]
        last_day = ref.replace(day=last_day_num)

        days=[]
        current = first_day
        while current <= last_day:
            days.append(current)
            current = date(current.year, current.month, current.day + 1)

        return days
    
    def group_horarios_by_day(self, rows: Sequence, tags_by_iniciativa: Mapping[str, List[TagSchema]]) -> Dict[date, List[CalendarioIniciativaItem]]:
        """
        Constrói itens (um por horário) e agrupa por data_evento.
        Ordena dentro do dia por (hora_inicio ASC, titulo ASC).
        Preenche tags a partir de tags_by_iniciativa.
        """

        grouped = {}

        for row in rows:
            item = CalendarioIniciativaItem(
                iniciativa_id=row.iniciativa_id,
                horario_id=row.horario_id,
                titulo=row.titulo,
                descricao=row.descricao,
                hora_inicio=row.hora_inicio,
                hora_fim=row.hora_fim,
                tipo=row.tipo,
                link=row.link,
                local=row.local,
                imagem_url=row.imagem_url,
                destaque=row.destaque,
                tags=tags_by_iniciativa.get(row.iniciativa_id, [])
            )

            data_evento = row.data_evento
            if data_evento not in grouped:
                grouped[data_evento] = []
            grouped[data_evento].append(item)

        for data_evento in grouped:
            grouped[data_evento].sort(key=lambda x: (x.hora_inicio, x.titulo))

        return grouped

    def build_calendario_response(self, ref: date, rows: Sequence, tags_by_iniciativa: Mapping[str, List[TagSchema]]) -> CalendarioMensalResponse:
        """
        Gera um esqueleto (todos os dias), agrupa itens e
        retorna o DTO final com mes="YYYY-MM" e lista de DiaCalendario.
        """

        month_days = self.build_month_days(ref)

        grouped_horarios = self.group_horarios_by_day(rows, tags_by_iniciativa)

        dias = []
        for day in month_days:
            iniciativas = grouped_horarios.get(day, [])
            dias.append(DiaCalendario(
                data=day, 
                iniciativas=iniciativas
            ))
        
        return CalendarioMensalResponse(
            mes=f"{ref.year:04d}-{ref.month:02d}",
            dias=dias
        )

