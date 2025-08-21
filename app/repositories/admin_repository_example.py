from datetime import datetime

from fastapi import HTTPException

from app.schemas.admin_schema_example import AdminCreate

admins_db: list[dict] = []


class AdminRepository:
    def create(self, admin_data: AdminCreate):
        if self.get_admin_by_email(admin_data.email):
            raise HTTPException(status_code=400, detail="Email já está em uso")

        new_admin = {
            "id": len(admins_db) + 1,
            "username": admin_data.username,
            "email": admin_data.email,
            "created_at": datetime.now(),
        }
        admins_db.append(new_admin)
        return new_admin

    def get_all(self):
        return admins_db

    def get_admin_by_id(self, admin_id: int):
        return next((admin for admin in admins_db if admin["id"] == admin_id), None)

    def get_admin_by_email(self, admin_email: str):
        return next(
            (admin for admin in admins_db if admin["email"] == admin_email), None
        )
