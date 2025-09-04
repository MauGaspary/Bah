import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.main import app
from app.models.admin_model_example import Base as AdminBase
from app.models.admin_iniciativa_model import AdminIniciativa, AdminTag, AdminIniciativaTag, Base as IniciativaBase

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
    IniciativaBase.metadata.create_all(bind=engine)
    yield
    AdminBase.metadata.drop_all(bind=engine)
    IniciativaBase.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_global(client):
    """Fixture que cria um admin para usar em testes"""
    admin_data = {"username": "test_admin", "email": "test_admin@example.com"}
    response = client.post("/admin/", json=admin_data)
    return response.json()


@pytest.fixture
def db_seed():
    """Fixture que popula o banco com dados de teste para iniciativas"""
    db = TestingSessionLocal()
    
    try:
        # Criar tags
        tag1 = AdminTag(nome="educacao")
        tag2 = AdminTag(nome="saude")
        tag3 = AdminTag(nome="tecnologia")
        
        db.add_all([tag1, tag2, tag3])
        db.commit()
        
        # Criar iniciativas
        iniciativa1 = AdminIniciativa(
            id="init-1",
            titulo="Projeto Educação Digital",
            descricao="Projeto para digitalizar a educação",
            status="ativa"
        )
        
        iniciativa2 = AdminIniciativa(
            id="init-2", 
            titulo="Portal de Saúde",
            descricao="Portal para gestão de saúde pública",
            status="encerrada"
        )
        
        iniciativa3 = AdminIniciativa(
            id="init-3",
            titulo="Inovação Tecnológica",
            descricao="Hub de inovação e tecnologia",
            status="ativa"
        )
        
        iniciativa4 = AdminIniciativa(
            id="init-4",
            titulo="Projeto Cancelado",
            descricao="Este projeto foi cancelado",
            status="cancelada"
        )
        
        db.add_all([iniciativa1, iniciativa2, iniciativa3, iniciativa4])
        db.commit()
        
        # Associar tags às iniciativas
        iniciativa1.tags.append(tag1)
        iniciativa1.tags.append(tag3)
        iniciativa2.tags.append(tag2)
        iniciativa3.tags.append(tag3)
        
        db.commit()
        
        yield
        
    finally:
        db.close()
