from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.demo_model import Demo
from app.schemas.demo_schema import DemoCreate


class DemoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, demo_data: DemoCreate):
        if self.get_demo_by_email(demo_data.email):
            raise HTTPException(status_code=400, detail="Email já está em uso")

        db_demo = Demo(username=demo_data.username, email=demo_data.email)
        self.db.add(db_demo)
        self.db.commit()
        self.db.refresh(db_demo)
        return db_demo

    def get_all(self):
        return self.db.query(Demo).all()

    def get_demo_by_id(self, demo_id: int):
        return self.db.query(Demo).filter(Demo.id == demo_id).first()

    def get_demo_by_email(self, demo_email: str):
        return self.db.query(Demo).filter(Demo.email == demo_email).first()
