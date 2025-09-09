import os

os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

if os.getenv("DOCKER_ENV") == "true":
    os.environ["TESTCONTAINERS_HOST_OVERRIDE"] = "host.docker.internal"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.config.database import get_db
from app.config.integration_settings import get_integration_test_settings
from app.main import create_app


@pytest.fixture(scope="session")
def postgres_container():
    """Container PostgreSQL para testes unitários"""
    with PostgresContainer("postgres:15") as postgres:
        if os.getenv("DOCKER_ENV") == "true":
            url = postgres.get_connection_url().replace(
                "localhost", "host.docker.internal"
            )
            postgres.get_connection_url = lambda: url
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    """Engine de teste com PostgreSQL"""
    database_url = postgres_container.get_connection_url()
    engine = create_engine(database_url)

    from tests.scripts.setup_test_db import setup_test_database

    setup_test_database(database_url)

    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Sessão de banco com transação e rollback"""
    connection = test_engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = session_factory()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, postgres_container):
    """Cliente de teste FastAPI usando PostgreSQL"""

    def override_get_db():
        yield db_session

    database_url = postgres_container.get_connection_url()
    settings = get_integration_test_settings(database_url)
    app = create_app(settings)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def admin_global(db_session):
    """Fixture que cria um admin para usar em testes"""
    from app.models.admin_model_example import Admin

    admin = Admin(username="test_admin", email="test_admin@example.com")
    db_session.add(admin)
    db_session.flush()

    return {"id": admin.id, "username": admin.username, "email": admin.email}


@pytest.fixture
def app_with_lifespan(postgres_container):
    """Fixture que cria app com lifespan para testes específicos"""
    database_url = postgres_container.get_connection_url()
    settings = get_integration_test_settings(database_url)
    app = create_app(settings)
    return app


# Fixtures para testes de auth/login
@pytest.fixture
def test_user(db_session):
    """Fixture que cria um usuário de teste no banco"""
    import uuid

    from app.models.user_model import User
    from app.utils.password_hasher import PasswordHasher

    hasher = PasswordHasher()
    user = User(
        id=uuid.uuid4(),
        email="teste@gmail.com",
        password_hash=hasher.hash("senha123"),
        name="Usuario Teste",
    )

    db_session.add(user)
    db_session.flush()
    return user
