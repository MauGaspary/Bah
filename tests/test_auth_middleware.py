import pytest
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Request
from fastapi.testclient import TestClient

from app.main import app
from app.config.settings import JWT_SECRET, JWT_ISS
from app.services.auth_middleware import jwt_required

VALID_USER = {
    "email": "teste@gmail.com",
    "password": "senha123"
}


@pytest.fixture
def client_with_test_route():
    """rota do middleware"""
    
    @app.get("/temp-middleware-test")
    @jwt_required
    async def temp_protected_route(request: Request):
        return {
            "userId": request.state.user["userId"],
            "email": request.state.user["email"],
            "iat": request.state.user["iat"]
        }
    
    yield TestClient(app)
    

def get_valid_token(test_user, client):
    response = client.post("/auth/login", json=VALID_USER)
    assert response.status_code == 200
    return response.json()["access_token"]


def create_expired_token():
    exp = datetime.now(timezone.utc) - timedelta(minutes=10)
    payload = {
        "sub": "test-user-id",
        "email": "teste@gmail.com",
        "iss": JWT_ISS,
        "iat": datetime.now(timezone.utc),
        "exp": exp
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def create_invalid_iss_token():
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        "sub": "test-user-id",
        "email": "teste@gmail.com",
        "iss": "issuer-errado", 
        "iat": datetime.now(timezone.utc),
        "exp": exp
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def create_invalid_signature_token():
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        "sub": "test-user-id", 
        "email": "teste@gmail.com",
        "iss": JWT_ISS,
        "iat": datetime.now(timezone.utc),
        "exp": exp
    }
    return jwt.encode(payload, "secret-errado", algorithm="HS256")


class TestAuthMiddleware:

    def test_protected_endpoint_without_token(self, client_with_test_route):
        response = client_with_test_route.get("/temp-middleware-test")
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid header"

    def test_protected_endpoint_invalid_authorization_header(self, client_with_test_route):
        headers = {"Authorization": "apenas-token"}
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid header"

    def test_protected_endpoint_malformed_token(self, client_with_test_route):
        headers = {"Authorization": "Bearer token_errado"}
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_protected_endpoint_expired_token(self, client_with_test_route):
        expired_token = create_expired_token()
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_protected_endpoint_invalid_issuer(self, client_with_test_route):
        invalid_iss_token = create_invalid_iss_token()
        headers = {"Authorization": f"Bearer {invalid_iss_token}"}
        
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_protected_endpoint_invalid_signature(self, client_with_test_route):
        invalid_sig_token = create_invalid_signature_token()
        headers = {"Authorization": f"Bearer {invalid_sig_token}"}
        
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_protected_endpoint_valid_token(self, test_user, client_with_test_route):
        valid_token = get_valid_token(test_user, client_with_test_route)
        headers = {"Authorization": f"Bearer {valid_token}"}
        
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 200
        
        data = response.json()
        assert "userId" in data
        assert "email" in data
        assert data["email"] == "teste@gmail.com"
        
        assert isinstance(data["userId"], str)
        assert len(data["userId"]) > 0

    def test_middleware_preserves_user_data(self, test_user, client_with_test_route):
        login_response = client_with_test_route.post("/auth/login", json=VALID_USER)
        token_data = login_response.json()
        
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 200
        
        user_data = response.json()
        assert user_data["email"] == VALID_USER["email"]
        
        assert isinstance(user_data["userId"], str)

    def test_authorization_header_case_sensitive(self, test_user, client_with_test_route):
        valid_token = get_valid_token(test_user, client_with_test_route)
        
        headers = {"Authorization": f"bearer {valid_token}"}
        response = client_with_test_route.get("/temp-middleware-test", headers=headers)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid header"
