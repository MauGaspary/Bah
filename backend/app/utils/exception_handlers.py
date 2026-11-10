from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import (
    DomainException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    ResourceNotFoundException,
)


async def domain_exception_handler(request: Request, exc: DomainException):
    if isinstance(exc, EmailAlreadyExistsException):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    if isinstance(exc, InvalidCredentialsException):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    if isinstance(exc, ResourceNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
