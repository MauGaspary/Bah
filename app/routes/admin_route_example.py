from fastapi import APIRouter

from app.controllers.admin_controller_example import AdminController
from app.schemas.admin_schema_example import AdminCreate, AdminResponse

router = APIRouter()
controller = AdminController()


@router.post("/", response_model=AdminResponse)
def create_admin(admin: AdminCreate):
    return controller.create_admin(admin)


@router.get("/", response_model=list[AdminResponse])
def get_admins():
    return controller.get_all_admins()


@router.get("/id/{admin_id}", response_model=AdminResponse)
def get_admin_by_id(admin_id: int):
    return controller.get_admin_by_id(admin_id)


@router.get("/email/{admin_email}", response_model=AdminResponse)
def get_admin_by_email(admin_email: str):
    return controller.get_admin_by_email(admin_email)
