from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.demo_schema import DemoCreate, DemoResponse
from app.services.demo_service import DemoService
from app.utils.exceptions import EmailAlreadyExistsException, ResourceNotFoundException


class DemoController:
    def __init__(self, db: Session):
        self.service = DemoService(db)

    def create_demo(self, demo_data: DemoCreate) -> DemoResponse:
        try:
            return self.service.create_demo(demo_data)
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
        except EmailAlreadyExistsException as e:
            raise HTTPException(400, str(e)) from e

    def get_all_demos(self) -> list[DemoResponse]:
        return self.service.get_all_demos()

    def get_demo_by_id(self, demo_id: int) -> DemoResponse:
        try:
            return self.service.get_demo_by_id(demo_id)
        except ResourceNotFoundException as e:
            raise HTTPException(404, str(e)) from e

    def get_demo_by_email(self, demo_email: str) -> DemoResponse:
        try:
            return self.service.get_demo_by_email(demo_email)
        except ResourceNotFoundException as e:
            raise HTTPException(404, str(e)) from e
