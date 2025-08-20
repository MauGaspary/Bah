from fastapi import HTTPException

from app.repositories.admin_repository_example import AdminRepository
from app.schemas.admin_schema_example import AdminCreate
from app.utils.helpers import validate_email


class AdminService:
    def __init__(self):
        self.repository = AdminRepository()

    def create_admin(self, admin_data: AdminCreate):
        if not validate_email(admin_data.email):
            raise HTTPException(status_code=400, detail="Formato de email inválido")

        return self.repository.create(admin_data)

    def get_all_admins(self):
        return self.repository.get_all()
