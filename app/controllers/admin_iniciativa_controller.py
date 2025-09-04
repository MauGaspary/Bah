from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.schemas.admin_iniciativa_schemas import IniciativaSchema
from app.services.admin_iniciativa_service import AdminIniciativaService
from app.config.database import get_db

router = APIRouter(prefix="/admin/iniciativas", tags=["Admin Iniciativas"])


@router.get("", response_model=dict)
def listar_iniciativas(
    q: Optional[str] = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    order_by: str = Query("criado_em"),
    order_dir: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return AdminIniciativaService.listar_iniciativas(
        db, q, created_from, created_to, order_by, order_dir, page, size
    )
