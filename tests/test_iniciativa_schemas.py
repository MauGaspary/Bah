from datetime import date
from datetime import time as dtime

import pytest

from app.models.iniciativa_horario_model import HorarioTipo
from app.schemas.iniciativa_schema import (
    IniciativaHorarioCreate,
    IniciativaHorarioPatch,
)


def test_horario_create_fim_deve_ser_depois_de_inicio():
    with pytest.raises(ValueError):
        IniciativaHorarioCreate(
            data_evento=date.today(),
            hora_inicio=dtime(10, 0),
            hora_fim=dtime(9, 0),
            tipo=HorarioTipo.PRESENCIAL,
        )


def test_horario_patch_data_nao_retroativa():
    with pytest.raises(ValueError):
        IniciativaHorarioPatch(data_evento=date(2000, 1, 1))
