from sqlalchemy.orm import Session
from datetime import date

from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse, CalendarioMensalResponse
from app.services.iniciativa_service import IniciativaService


class IniciativaController:
    def __init__(self, db: Session):
        self.service = IniciativaService(db)

    def create_iniciativa(
        self, iniciativa_data: IniciativaCreate, criado_por: str
    ) -> IniciativaResponse:
        return self.service.create_iniciativa(iniciativa_data, criado_por)

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        return self.service.get_iniciativa_by_id(iniciativa_id)

    def get_calendario_mensal(self, data: date) -> CalendarioMensalResponse:
        return self.service.get_calendario_mensal(data)