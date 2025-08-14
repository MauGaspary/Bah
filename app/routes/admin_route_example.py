from fastapi import APIRouter
from app.schemas.admin_schema_example import AdminCreate, AdminResponse
from app.controllers.admin_controller_example import AdminController

router = APIRouter()
controller = AdminController()

@router.post("/", response_model=AdminResponse)
def create_admin(admin: AdminCreate):
    return controller.create_admin(admin)

@router.get("/", response_model=list[AdminResponse])
def get_admins():
    return controller.get_all_admins()