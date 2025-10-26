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
