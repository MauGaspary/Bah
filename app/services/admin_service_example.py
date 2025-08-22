from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.admin_repository_example import AdminRepository
from app.schemas.admin_schema_example import AdminCreate
from app.utils.helpers import validate_email


class AdminService:
    def __init__(self, db: Session):
        self.repository = AdminRepository(db)

    def create_admin(self, admin_data: AdminCreate):
        if not validate_email(admin_data.email):
            raise HTTPException(status_code=400, detail="Formato de email inválido")

        return self.repository.create(admin_data)

    def get_all_admins(self):
        return self.repository.get_all()

    def get_admin_by_id(self, admin_id: int):
        admin = self.repository.get_admin_by_id(admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin não encontrado")
        return admin

    def get_admin_by_email(self, admin_email: str):
        admin = self.repository.get_admin_by_email(admin_email)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin não encontrado")
        return admin
