from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse
from app.services.iniciativa_service import IniciativaService


class IniciativaController:
    def __init__(self, db: Session, model: SentenceTransformer = None):
        self.service = IniciativaService(db, model)

    def create_iniciativa(
        self,
        iniciativa_data: IniciativaCreate,
        criado_por: str,
    ) -> IniciativaResponse:
        return self.service.create_iniciativa(iniciativa_data, criado_por)

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        return self.service.get_iniciativa_by_id(iniciativa_id)
