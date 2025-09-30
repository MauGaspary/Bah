from http.client import HTTPException
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
        try:
            return self.service.create_iniciativa(iniciativa_data, criado_por)
        except ValueError as e:
            raise HTTPException(422, str(e)) from e
        except RuntimeError as e:
            raise HTTPException(500, str(e)) from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        return self.service.get_iniciativa_by_id(iniciativa_id)

    def search_iniciativas(self, query: str, page: int, size: int):
        try:
            return self.service.search_iniciativas(query, page, size)
        except HTTPException as e:
            raise e
