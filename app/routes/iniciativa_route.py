from datetime import date

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.iniciativa_controller import IniciativaController
from app.schemas.iniciativa_schema import (
    CalendarioMensalResponse,
    IniciativaCreate,
    IniciativaResponse,
)

security = HTTPBearer()

router = APIRouter()


@router.post(
    "/", response_model=IniciativaResponse, status_code=status.HTTP_201_CREATED
)
def create_iniciativa(
    iniciativa: IniciativaCreate,
    criado_por: str = "sistema",  # TODO: Obter do token de autenticação
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Cria uma nova iniciativa.

    Validações:
    - Todos os campos obrigatórios devem estar presentes
    - Organizador deve existir
    - Tags devem existir (se fornecidas)
    - Hora de fim deve ser maior que hora de início
    - Não deve haver duplicidade de título para o mesmo organizador

    Retorna 201 com o recurso criado ou 422 quando validações falham.
    """
    controller = IniciativaController(db)
    return controller.create_iniciativa(iniciativa, criado_por)


@router.get("/calendario", response_model=CalendarioMensalResponse)
def get_calendario_mensal(
    data: date = Query(..., description="Data de referência para o mês (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Retorna o calendário de iniciativas para o mês especificado.

    Parâmetros:
    - data: Data de referência (qualquer dia do mês desejado)

    Retorna:
    - Lista de dias do mês com iniciativas agrupadas por dia
    - Iniciativas ordenadas por horário e título
    - Dias sem iniciativas retornam lista vazia
    """

    controller = IniciativaController(db)
    return controller.get_calendario_mensal(data)


@router.get("/{iniciativa_id}", response_model=IniciativaResponse)
def get_iniciativa_by_id(
    iniciativa_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db)
    return controller.get_iniciativa_by_id(iniciativa_id)
