from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.model import get_embedding_model
from app.controllers.admin_iniciativa_controller import AdminIniciativaController
from app.controllers.iniciativa_controller import IniciativaController
from app.dependencies.auth import get_current_user
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse

security = HTTPBearer()

router = APIRouter()


@router.get(
    "/search",
    response_model=IniciativaListResponseSchema,
    status_code=status.HTTP_200_OK,
)
def search_iniciativas(
    q: str = Query(..., description="Texto da busca semântica"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
    model: SentenceTransformer = Depends(get_embedding_model),
):

    controller = IniciativaController(db, model)
    return controller.search_iniciativas(q, page, size)


@router.post(
    "/", response_model=IniciativaResponse, status_code=status.HTTP_201_CREATED
)
def create_iniciativa(
    iniciativa: IniciativaCreate,
    request: Request,
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
    model = request.app.state.embedding_model
    controller = IniciativaController(db, model)
    return controller.create_iniciativa(iniciativa, criado_por)


@router.get("/{iniciativa_id}", response_model=IniciativaResponse)
def get_iniciativa_by_id(
    iniciativa_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db)
    return controller.get_iniciativa_by_id(iniciativa_id)
