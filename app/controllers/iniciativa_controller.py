from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse
from app.services.iniciativa_service import IniciativaService


class IniciativaController:
    def __init__(self, db: Session, model: Optional[object] = None):
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
        try:
            return self.service.get_iniciativa_by_id(iniciativa_id)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    def search_iniciativas(self, query: str, page: int, size: int):
        try:
            return self.service.search_iniciativas(query, page, size)
        except HTTPException as e:
            raise e
