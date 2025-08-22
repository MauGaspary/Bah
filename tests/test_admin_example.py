import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.main import app
from app.models.admin_model_example import Base

# Banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_global():
    """Fixture que cria um admin para usar em testes"""
    admin_data = {"username": "test_admin", "email": "test_admin@example.com"}
    response = client.post("/admin/", json=admin_data)
    return response.json()


def test_create_admin():
    admin_data = {"username": "testuser", "email": "test@example.com"}

    response = client.post("/admin/", json=admin_data)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_admins():
    response = client.get("/admin/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_admin_by_id(admin_global):
    response = client.get(f"/admin/id/{admin_global['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_global["id"]


def test_get_admin_by_id_not_found():
    """Busca de admin com ID que nao existe"""
    response = client.get("/admin/id/9999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Admin não encontrado"


def test_get_admin_by_email(admin_global):
    response = client.get(f"/admin/email/{admin_global['email']}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == admin_global["email"]


def test_get_admin_by_email_not_found():
    """Busca de admin com email que nao existe"""
    response = client.get("/admin/email/nonexistent@example.com")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Admin não encontrado"
