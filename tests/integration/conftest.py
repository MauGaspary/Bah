import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.config.database import get_db
from app.config.integration_settings import get_integration_test_settings
from app.main import create_app
from app.models.admin_model_example import Base


@pytest.fixture(scope="session")
def postgres_container():
    """Container PostgreSQL para testes de integração"""
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


@pytest.fixture(scope="session")
def testing_session_local(test_engine):
    """Session factory para testes"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session(test_engine):
    """Sessão de banco com transação e rollback"""

    # Criar conexão e transação
    connection = test_engine.connect()
    transaction = connection.begin()

    # Criar sessão usando a conexão
    session_factory = sessionmaker(bind=connection)
    session = session_factory()

    yield session

    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, postgres_container):
    """Cliente de teste com override de dependência"""

    def override_get_db():
        yield db_session

    database_url = postgres_container.get_connection_url()
    settings = get_integration_test_settings(database_url)
    app = create_app(settings)
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture
def async_client(db_session, postgres_container):
    """AsyncClient com LifespanManager para testes assíncronos"""

    def override_get_db():
        yield db_session

    database_url = postgres_container.get_connection_url()
    settings = get_integration_test_settings(database_url)
    app = create_app(settings)
    app.dependency_overrides[get_db] = override_get_db

    return AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")
