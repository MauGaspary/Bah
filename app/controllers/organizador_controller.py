from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.organizador_schema import OrganizadorResponse
from app.services.organizador_service import OrganizadorService
from app.utils.exceptions import ResourceNotFoundException


class OrganizadorController:

    def __init__(self, db: Session):
        self.service = OrganizadorService(db)

    def list_all(self) -> List[OrganizadorResponse]:
        return self.service.list_all()

    def get_by_id(self, organizador_id: str) -> OrganizadorResponse:
        try:
            return self.service.get_by_id(organizador_id)
        except ResourceNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
