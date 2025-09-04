from fastapi import APIRouter
from app.controllers import admin_iniciativa_controller

router = APIRouter()
router.include_router(admin_iniciativa_controller.router)
