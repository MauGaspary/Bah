from typing import List

from sqlalchemy.orm import Session

from app.repositories.organizador_repository import OrganizadorRepository
from app.schemas.organizador_schema import OrganizadorResponse
from app.utils.exceptions import ResourceNotFoundException


class OrganizadorService:

    def __init__(self, db: Session):
        self.repository = OrganizadorRepository(db)

    def list_all(self) -> List[OrganizadorResponse]:
        organizadores = self.repository.list_all()
        return [OrganizadorResponse.model_validate(org) for org in organizadores]

    def get_by_id(self, organizador_id: str) -> OrganizadorResponse:
        organizador = self.repository.get_by_id(organizador_id)
        if not organizador:
            raise ResourceNotFoundException(
                f"Organizador com ID {organizador_id} não encontrado"
            )
        return OrganizadorResponse.model_validate(organizador)
