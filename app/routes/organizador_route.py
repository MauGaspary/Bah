from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.organizador_model import Organizador

router = APIRouter()


@router.get("/")
def listar_organizadores(db: Session = Depends(get_db)):
    """Lista todos os organizadores disponíveis."""
    organizadores = db.query(Organizador).all()
    return [{"id": org.id, "nome": org.nome} for org in organizadores]
