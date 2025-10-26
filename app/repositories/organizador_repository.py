from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.organizador_model import Organizador


class OrganizadorRepository:

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> List[Organizador]:
        return self.session.query(Organizador).all()

    def get_by_id(self, organizador_id: str) -> Optional[Organizador]:
        return (
            self.session.query(Organizador)
            .filter(Organizador.id == organizador_id)
            .first()
        )

    def create(self, organizador: Organizador) -> Organizador:
        self.session.add(organizador)
        self.session.commit()
        self.session.refresh(organizador)
        return organizador

    def update(self, organizador: Organizador) -> Organizador:
        self.session.commit()
        self.session.refresh(organizador)
        return organizador

    def delete(self, organizador: Organizador) -> None:
        self.session.delete(organizador)
        self.session.commit()
