from app.schemas.admin_schema_example import AdminCreate, AdminResponse
from app.services.admin_service_example import AdminService


class AdminController:
    def __init__(self):
        self.service = AdminService()

    def create_admin(self, admin_data: AdminCreate) -> AdminResponse:
        return self.service.create_admin(admin_data)

    def get_all_admins(self) -> list[AdminResponse]:
        return self.service.get_all_admins()

    def get_admin_by_id(self, admin_id: int) -> AdminResponse:
        return self.service.get_admin_by_id(admin_id)

    def get_admin_by_email(self, admin_email: str) -> AdminResponse:
        return self.service.get_admin_by_email(admin_email)
