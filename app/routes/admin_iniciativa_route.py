from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.config.database import get_db
from app.controllers.admin_iniciativa_controller import AdminIniciativaController
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema

router = APIRouter()


@router.get("/iniciativas", response_model=IniciativaListResponseSchema)
def listar_iniciativas(
    q: Optional[str] = Query(None, description="Busca por titulo, descricao ou tags"),
    created_from: Optional[datetime] = Query(None, description="Data de criacao inicial (YYYY-MM-DD)"),
    created_to: Optional[datetime] = Query(None, description="Data de criacao final (YYYY-MM-DD)"),
    order_by: str = Query("criado_em", description="Campo para ordenacao", regex="criado_em|titulo|destaque|editado_em"),
    order_dir: str = Query("desc", description="Direcao da ordenacao", regex="asc ou desc"),
    page: int = Query(1, ge=1, description="Numero da pagina"),
    size: int = Query(10, ge=1, le=100, description="Itens por pagina"),
    db: Session = Depends(get_db)
):
    controller = AdminIniciativaController(db)
    return controller.listar_iniciativas(q, created_from, created_to, order_by, order_dir, page, size)
