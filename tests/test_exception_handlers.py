import pytest
from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exception_handlers import domain_exception_handler, value_error_handler
from app.utils.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    ResourceNotFoundException,
)


@pytest.fixture
def mock_request():
    """Mock request for testing"""
    return Request({"type": "http", "method": "GET", "url": "http://test"})


@pytest.mark.asyncio
async def test_email_already_exists_handler(mock_request):
    """Test handler for EmailAlreadyExistsException"""
    exc = EmailAlreadyExistsException("Email já existe")

    response = await domain_exception_handler(mock_request, exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_credentials_handler(mock_request):
    """Test handler for InvalidCredentialsException"""
    exc = InvalidCredentialsException("Credenciais inválidas")

    response = await domain_exception_handler(mock_request, exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_resource_not_found_handler(mock_request):
    """Test handler for ResourceNotFoundException"""
    exc = ResourceNotFoundException("Recurso não encontrado")

    response = await domain_exception_handler(mock_request, exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_value_error_handler(mock_request):
    """Test handler for ValueError"""
    exc = ValueError("Valor inválido")

    response = await value_error_handler(mock_request, exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
