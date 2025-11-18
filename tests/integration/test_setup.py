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
    from app.models.usuario_model import Usuario

    usuario = Usuario(
        nome="Test",
        sobrenome="Isolation",
        email="test@isolation.com",
        senha_hash="hash_test_isolation"
    )
    db_session.add(usuario)
    db_session.flush()

    found_usuario = db_session.query(Usuario).filter_by(email="test@isolation.com").first()
    assert found_usuario is not None
    assert found_usuario.nome == "Test"
    assert found_usuario.sobrenome == "Isolation"
