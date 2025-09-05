from fastapi import APIRouter, Request
from app.services.auth_middleware import jwt_required


router = APIRouter(prefix="/test", tags=["test"])

@router.get("/protected")
@jwt_required
async def protected(request: Request):
    return {
        "userId": request.state.user["userId"],
        "email": request.state.user["email"],
    }