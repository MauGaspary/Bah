from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.admin_iniciativa_controller import AdminIniciativaController
from app.controllers.iniciativa_controller import IniciativaController
from app.dependencies.auth import get_current_user
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse

router = APIRouter()


@router.post(
    "/iniciativas/",
    response_model=IniciativaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_iniciativa(
    iniciativa: IniciativaCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Cria uma nova iniciativa."""
    controller = IniciativaController(db)
    return controller.create_iniciativa(iniciativa, current_user)


@router.get("/iniciativas/{iniciativa_id}", response_model=IniciativaResponse)
def get_iniciativa_by_id(
    iniciativa_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db)
    return controller.get_iniciativa_by_id(iniciativa_id)


@router.get("/iniciativas", response_model=IniciativaListResponseSchema)
def listar_iniciativas(
    q: Optional[str] = Query(None, description="Busca por titulo, descricao ou tags"),
    created_from: Optional[datetime] = Query(
        None, description="Data de criacao inicial (YYYY-MM-DD)"
    ),
    created_to: Optional[datetime] = Query(
        None, description="Data de criacao final (YYYY-MM-DD)"
    ),
    order_by: str = Query(
        "criado_em",
        description="Campo para ordenacao",
        pattern="^(criado_em|titulo|destaque|editado_em)$",
    ),
    order_dir: str = Query(
        "desc", description="Direcao da ordenacao", pattern="^(asc|desc)$"
    ),
    page: int = Query(1, ge=1, description="Numero da pagina"),
    size: int = Query(10, ge=1, le=100, description="Itens por pagina"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = AdminIniciativaController(db)
    return controller.listar_iniciativas(
        q, created_from, created_to, order_by, order_dir, page, size
    )
