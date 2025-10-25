from typing import List

from sqlalchemy.orm import Session

from app.repositories.organizador_repository import OrganizadorRepository
from app.schemas.organizador_schema import OrganizadorResponse


class OrganizadorService:

    def __init__(self, db: Session):
        self.repository = OrganizadorRepository(db)

    def list_all(self) -> List[OrganizadorResponse]:
        organizadores = self.repository.list_all()
        return [OrganizadorResponse.model_validate(org) for org in organizadores]
