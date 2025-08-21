from app.main import root


def test_root_function():
    """Testa a função root diretamente"""
    result = root()
    assert result == {"message": "Bah – Plataforma de Inovação de Caxias do Sul"}
