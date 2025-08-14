from app.repositories.admin_repository_example import AdminRepository
from app.schemas.admin_schema_example import AdminCreate

class AdminService:
    def __init__(self):
        self.repository = AdminRepository()
    
    def create_admin(self, admin_data: AdminCreate):
        return self.repository.create(admin_data)
    
    def get_all_admins(self):
        return self.repository.get_all()