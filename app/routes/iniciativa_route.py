from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.iniciativa_controller import IniciativaController
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse

router = APIRouter()


@router.post(
    "/", response_model=IniciativaResponse, status_code=status.HTTP_201_CREATED
)
def create_iniciativa(
    iniciativa: IniciativaCreate,
    criado_por: str = "sistema",  # TODO: Obter do token de autenticação
    db: Session = Depends(get_db),
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


@router.get("/{iniciativa_id}", response_model=IniciativaResponse)
def get_iniciativa_by_id(iniciativa_id: str, db: Session = Depends(get_db)):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db)
    return controller.get_iniciativa_by_id(iniciativa_id)
