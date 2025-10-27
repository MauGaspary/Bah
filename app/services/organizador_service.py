from typing import List

from sqlalchemy.orm import Session

from app.models.organizador_model import Organizador
from app.repositories.organizador_repository import OrganizadorRepository
from app.schemas.organizador_schema import (
    OrganizadorCreate,
    OrganizadorResponse,
    OrganizadorUpdate,
)
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

    def create(self, organizador_data: OrganizadorCreate) -> OrganizadorResponse:
        organizador = Organizador(
            nome=organizador_data.nome,
        )
        created_organizador = self.repository.create(organizador)
        return OrganizadorResponse.model_validate(created_organizador)

    def update(
        self, organizador_id: str, organizador_data: OrganizadorUpdate
    ) -> OrganizadorResponse:
        organizador = self.repository.get_by_id(organizador_id)
        if not organizador:
            raise ResourceNotFoundException(
                f"Organizador com ID {organizador_id} não encontrado"
            )

        if organizador_data.nome is not None:
            organizador.nome = organizador_data.nome

        updated_organizador = self.repository.update(organizador)
        return OrganizadorResponse.model_validate(updated_organizador)

    def delete(self, organizador_id: str) -> None:
        organizador = self.repository.get_by_id(organizador_id)
        if not organizador:
            raise ResourceNotFoundException(
                f"Organizador com ID {organizador_id} não encontrado"
            )
        self.repository.delete(organizador)
