from sqlalchemy.orm import Session

from app.schemas.demo_schema import DemoCreate, DemoResponse
from app.services.demo_service import DemoService


class DemoController:
    def __init__(self, db: Session):
        self.service = DemoService(db)

    def create_demo(self, demo_data: DemoCreate) -> DemoResponse:
        return self.service.create_demo(demo_data)

    def get_all_demos(self) -> list[DemoResponse]:
        return self.service.get_all_demos()

    def get_demo_by_id(self, demo_id: int) -> DemoResponse:
        return self.service.get_demo_by_id(demo_id)

    def get_demo_by_email(self, demo_email: str) -> DemoResponse:
        return self.service.get_demo_by_email(demo_email)
