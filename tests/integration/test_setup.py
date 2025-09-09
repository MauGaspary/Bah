import pytest
from sqlalchemy import text


@pytest.mark.integration
def test_database_connection(db_session):
    """Testa se a conexão com o banco está funcionando"""
    result = db_session.execute(text("SELECT 1 as test"))
    assert result.fetchone()[0] == 1


@pytest.mark.integration
def test_transaction_isolation(db_session):
    """Testa se o isolamento de transações está funcionando"""
    from app.models.demo_model import Demo

    demo = Demo(username="test_isolation", email="test@isolation.com")
    db_session.add(demo)
    db_session.flush()

    found_demo = db_session.query(Demo).filter_by(email="test@isolation.com").first()
    assert found_demo is not None
    assert found_demo.username == "test_isolation"
