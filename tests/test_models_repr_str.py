from app.models.descricoes_extras_model import DescricoesExtras
from app.models.iniciativa_model import Iniciativa


def test_repr_str_iniciativa_sem_db_nao_explode():
    i = Iniciativa()
    assert isinstance(repr(i), str)
    assert isinstance(str(i), str)


def test_repr_str_descricoes_extras_sem_db_nao_explode():
    d = DescricoesExtras()
    assert isinstance(repr(d), str)
    assert isinstance(str(d), str)
