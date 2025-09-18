from sqlalchemy.orm import Session

from app.repositories.demo_repository import DemoRepository
from app.schemas.demo_schema import DemoCreate
from app.utils.exceptions import ResourceNotFoundException
from app.utils.helpers import validate_email


class DemoService:
    def __init__(self, db: Session):
        self.repository = DemoRepository(db)

    def create_demo(self, demo_data: DemoCreate):
        if not validate_email(demo_data.email):
            raise ValueError("Formato de email inválido")

        return self.repository.create(demo_data)

    def get_all_demos(self):
        return self.repository.get_all()

    def get_demo_by_id(self, demo_id: int):
        demo = self.repository.get_demo_by_id(demo_id)
        if not demo:
            raise ResourceNotFoundException("Demo não encontrado")
        return demo

    def get_demo_by_email(self, demo_email: str):
        demo = self.repository.get_demo_by_email(demo_email)
        if not demo:
            raise ResourceNotFoundException("Demo não encontrado")
        return demo
