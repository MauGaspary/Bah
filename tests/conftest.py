import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.config.settings import get_test_settings
from app.main import create_app
from app.models.admin_model_example import Base

# Banco para testes unitários
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = testing_session_local()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    """Cliente de teste FastAPI usando create_app"""
    settings = get_test_settings()
    app = create_app(settings)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup e teardown do banco para cada teste"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_global(client):
    """Fixture que cria um admin para usar em testes"""
    admin_data = {"username": "test_admin", "email": "test_admin@example.com"}
    response = client.post("/admin/", json=admin_data)
    return response.json()


@pytest.fixture
def app_with_lifespan():
    """Fixture que cria app com lifespan para testes específicos"""
    settings = get_test_settings()
    app = create_app(settings)
    app.dependency_overrides[get_db] = override_get_db
    return app
