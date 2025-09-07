import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.config.database import get_db
from app.config.integration_settings import get_integration_test_settings
from app.main import create_app
from tests.helpers import request


@pytest.fixture(scope="session")
def postgres_container():
    """Container PostgreSQL para testes unitários"""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    """Engine de teste com PostgreSQL"""
    database_url = postgres_container.get_connection_url()
    engine = create_engine(database_url)

    # Executar migrations usando Alembic
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
