import os

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.config.integration_settings import get_integration_test_settings
from app.main import create_app


def is_docker_available():
    """Verifica se Docker está disponível"""
    try:
        import docker

        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


use_containers_env = os.getenv("USE_CONTAINERS", "auto").lower()
if use_containers_env == "auto":
    USE_CONTAINERS = is_docker_available()
    MODE_MSG = (
        "Docker detectado: Usando PostgreSQL containers"
        if USE_CONTAINERS
        else "Usando SQLite local"
    )
else:
    USE_CONTAINERS = use_containers_env == "true"
    MODE_MSG = (
        "Forçando uso de Docker PostgreSQL containers"
        if USE_CONTAINERS
        else "Usando SQLite local"
    )

print(f"\n{MODE_MSG}\n", flush=True)

if USE_CONTAINERS:
    from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container():
    """Container PostgreSQL para testes de integração"""
    if not USE_CONTAINERS:

        class MockContainer:
            def get_connection_url(self):
                return "sqlite:///:memory:"

        yield MockContainer()
    else:
        with PostgresContainer("pgvector/pgvector:pg15") as postgres:
            yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    """Engine de teste com PostgreSQL ou SQLite"""
    database_url = postgres_container.get_connection_url()

    if USE_CONTAINERS:
        engine = create_engine(database_url)
        from tests.scripts.setup_test_db import setup_test_database

        setup_test_database(database_url)
    else:
        engine = create_engine(
            "sqlite:///:memory:", connect_args={"check_same_thread": False}
        )
        from app.models.base import Base

        Base.metadata.create_all(bind=engine)

    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def testing_session_local(test_engine):
    """Session factory para testes"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


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
