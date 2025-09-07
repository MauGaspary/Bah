import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.jwt_service import verify
from app.config.settings import JWT_TTL
import bcrypt

client = TestClient(app)

VALID_USER = {
    "email": "teste@gmail.com",
    "password": "senha123"
}

INVALID_USER = {
    "email": "naoexiste@gmail.com",
    "password": "qualquer"
}

def test_login_success(test_user):
    response = client.post("/auth/login", json=VALID_USER)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == JWT_TTL
    
    
    claims = verify(data["access_token"])
    assert claims["email"] == VALID_USER["email"]

def test_login_invalid_credentials():
    response = client.post("/auth/login", json=INVALID_USER)
    assert response.status_code == 401