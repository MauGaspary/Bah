from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse
from app.services.iniciativa_service import IniciativaService


class IniciativaController:
    def __init__(self, db: Session):
        self.service = IniciativaService(db)

    def create_iniciativa(
        self, iniciativa_data: IniciativaCreate, criado_por: str
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
        except ValueError as e:
            raise HTTPException(404, str(e)) from e
