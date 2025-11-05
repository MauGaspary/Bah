from datetime import date, time, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.iniciativa_schema import IniciativaCreate


def _amanha():
    return date.today() + timedelta(days=1)


def _horario(ok=True):
    if ok:
        return {"data": _amanha(), "hora_inicio": time(9, 0), "hora_fim": time(10, 0)}

    return {"data": _amanha(), "hora_inicio": time(9, 0), "hora_fim": time(9, 0)}


def test_iniciativa_titulo_apenas_espacos_rejeita():
    with pytest.raises(ValidationError):
        IniciativaCreate(
            titulo="   ",
            descricao="ok",
            local="ok",
            horarios=[_horario()],
            tags_ids=[],
        )


def test_iniciativa_horario_inicio_igual_fim_rejeita():
    with pytest.raises(ValidationError):
        IniciativaCreate(
            titulo="ok",
            descricao="ok",
            local="ok",
            horarios=[_horario(ok=False)],
            tags_ids=[],
        )


def test_iniciativa_tags_duplicadas_rejeita():

    dup = "11111111-1111-1111-1111-111111111111"
    with pytest.raises(ValidationError):
        IniciativaCreate(
            titulo="ok",
            descricao="ok",
            local="ok",
            horarios=[_horario()],
            tags_ids=[dup, dup],
        )
