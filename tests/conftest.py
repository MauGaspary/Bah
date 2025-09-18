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
    from app.models.demo_model import Demo

    demo = Demo(username="test_admin", email="test_admin@example.com")
    db_session.add(demo)
    db_session.flush()

    return {"id": demo.id, "username": demo.username, "email": demo.email}


@pytest.fixture
def app_with_lifespan(postgres_container):
    """Fixture que cria app com lifespan para testes específicos"""
    database_url = postgres_container.get_connection_url()
    settings = get_integration_test_settings(database_url)
    app = create_app(settings)
    return app


@pytest.fixture
def usuario_fixture(db_session):
    """Fixture que cria um usuário para usar em testes"""
    import uuid

    from app.models.usuario_model import Usuario

    usuario = Usuario(
        id=str(uuid.uuid4()),
        nome="Usuário",
        sobrenome="Teste",
        email="usuario.teste@example.com",
        senha_hash="hash_senha_teste",
    )
    db_session.add(usuario)
    db_session.flush()

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "sobrenome": usuario.sobrenome,
        "email": usuario.email,
    }


@pytest.fixture
def organizador_fixture(db_session):
    """Fixture que cria um organizador para usar em testes"""
    import uuid

    from app.models.organizador_model import Organizador

    organizador = Organizador(id=str(uuid.uuid4()), nome="Organizador Teste")
    db_session.add(organizador)
    db_session.flush()

    return {"id": organizador.id, "nome": organizador.nome}


@pytest.fixture
def tag_fixture(db_session):
    """Fixture que cria uma tag para usar em testes"""
    import uuid

    from app.models.tag_model import Tag

    tag = Tag(id=str(uuid.uuid4()), nome="Tecnologia", descricao="Tag de tecnologia")
    db_session.add(tag)
    db_session.flush()

    return {"id": tag.id, "nome": tag.nome, "descricao": tag.descricao}


@pytest.fixture
def iniciativa_fixture(db_session, organizador_fixture, usuario_fixture):
    """Fixture que cria uma iniciativa para usar em testes"""
    from datetime import date, time

    import numpy as np

    from app.models.iniciativa_horario_model import HorarioTipo, IniciativaHorario
    from app.models.iniciativa_model import Iniciativa

    test_vector = np.random.rand(768).tolist()

    iniciativa = Iniciativa(
        titulo="Iniciativa Teste Existente",
        descricao="Descrição da iniciativa teste existente",
        descricao_vetor=test_vector,
        organizador_id=organizador_fixture["id"],
        link="https://example.com/existente",
        imagem_url="https://example.com/image-existente.jpg",
        destaque=False,
        criado_por=usuario_fixture["id"],
    )
    db_session.add(iniciativa)
    db_session.flush()

    horario = IniciativaHorario(
        iniciativa_id=iniciativa.id,
        data_evento=date(2025, 12, 15),
        hora_inicio=time(10, 0),
        hora_fim=time(16, 0),
        tipo=HorarioTipo.PRESENCIAL,
    )
    db_session.add(horario)
    db_session.flush()

    return {
        "id": iniciativa.id,
        "titulo": iniciativa.titulo,
        "organizador_id": iniciativa.organizador_id,
    }


@pytest.fixture
def auth_token(usuario_fixture):
    """Fixture que gera um token JWT válido para testes"""
    from app.services.jwt_service import sign

    return sign(usuario_fixture["id"], usuario_fixture["email"])


@pytest.fixture
def test_user(db_session):
    """Fixture que cria um usuário de teste para autenticação"""
    import uuid

    import bcrypt

    from app.models.usuario_model import Usuario

    password_hash = bcrypt.hashpw("senha123".encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    usuario = Usuario(
        id=str(uuid.uuid4()),
        nome="Teste",
        sobrenome="Usuario",
        email="teste@gmail.com",
        senha_hash=password_hash,
    )
    db_session.add(usuario)
    db_session.flush()

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
    }
