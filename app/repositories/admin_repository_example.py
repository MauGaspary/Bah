from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin_model_example import Admin
from app.schemas.admin_schema_example import AdminCreate


class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, admin_data: AdminCreate):
        if self.get_admin_by_email(admin_data.email):
            raise HTTPException(status_code=400, detail="Email já está em uso")

        db_admin = Admin(username=admin_data.username, email=admin_data.email)
        self.db.add(db_admin)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin

    def get_all(self):
        return self.db.query(Admin).all()

    def get_admin_by_id(self, admin_id: int):
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def get_admin_by_email(self, admin_email: str):
        return self.db.query(Admin).filter(Admin.email == admin_email).first()
