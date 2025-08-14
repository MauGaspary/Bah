from app.schemas.admin_schema_example import AdminCreate, AdminResponse
from app.services.admin_service_example import AdminService

class AdminController:
    def __init__(self):
        self.service = AdminService()
    
    def create_admin(self, admin_data: AdminCreate) -> AdminResponse:
        """Lógica do controller para criar admin"""
        return self.service.create_admin(admin_data)
    
    def get_all_admins(self) -> list[AdminResponse]:
        """Lógica do controller para listar admins"""
        return self.service.get_all_admins()