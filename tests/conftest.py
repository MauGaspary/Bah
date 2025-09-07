import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.main import app
from app.models.admin_model_example import Base as AdminBase
from app.models.user_model import Base as UserBase, User

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


@pytest.fixture(scope="session")
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup e teardown do banco para cada teste"""

    AdminBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
    yield

    AdminBase.metadata.drop_all(bind=engine)
    UserBase.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_global(client):
    """Fixture que cria um admin para usar em testes"""
    admin_data = {"username": "test_admin", "email": "test_admin@example.com"}
    response = client.post("/admin/", json=admin_data)
    return response.json()


@pytest.fixture
def test_user():
    """Fixture que cria um usuário de teste no banco"""
    import uuid
    from app.models.user_model import User
    from app.utils.passwordHasher import PasswordHasher
    hasher = PasswordHasher()

    user = User(
        id=uuid.uuid4(), 
        email="teste@gmail.com",
        password_hash=hasher.hash("senha123"),
        name="Usuario Teste"
    )
    

    db = TestingSessionLocal()
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()
