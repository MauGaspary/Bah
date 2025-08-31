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
    from app.models.admin_model_example import Admin

    # Criar um admin na sessão atual
    admin = Admin(username="test_isolation", email="test@isolation.com")
    db_session.add(admin)
    db_session.flush()  # Força o INSERT mas não commita

    # Verificar que o admin existe na sessão atual
    found_admin = db_session.query(Admin).filter_by(email="test@isolation.com").first()
    assert found_admin is not None
    assert found_admin.username == "test_isolation"
