from typing import List

from sqlalchemy.orm import Session

from app.schemas.organizador_schema import OrganizadorResponse
from app.services.organizador_service import OrganizadorService


class OrganizadorController:

    def __init__(self, db: Session):
        self.service = OrganizadorService(db)

    def list_all(self) -> List[OrganizadorResponse]:
        return self.service.list_all()
