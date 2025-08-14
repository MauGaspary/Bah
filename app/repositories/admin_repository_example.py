from app.schemas.admin_schema_example import AdminCreate
from datetime import datetime

admins_db = []

class AdminRepository:
    def create(self, admin_data: AdminCreate):
        new_admin = {
            "id": len(admins_db) + 1,
            "username": admin_data.username,
            "email": admin_data.email,
            "created_at": datetime.now()
        }
        admins_db.append(new_admin)
        return new_admin
    
    def get_all(self):
        return admins_db
    
    def find_by_username(self, username: str):
        return next((admin for admin in admins_db if admin["username"] == username), None)
    
    def find_by_id(self, admin_id: int):
        return next((admin for admin in admins_db if admin["id"] == admin_id), None)