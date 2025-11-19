from datetime import date
from datetime import time as dtime
from types import SimpleNamespace

from app.models.iniciativa_horario_model import HorarioTipo
from app.schemas.iniciativa_schema import TagSchema
from app.services.iniciativa_service import IniciativaService


def _row(iid, hid, titulo, dia, hi, hf, tipo=HorarioTipo.PRESENCIAL):
    return SimpleNamespace(
        iniciativa_id=iid,
        horario_id=hid,
        titulo=titulo,
        descricao="d",
        hora_inicio=hi,
        hora_fim=hf,
        tipo=tipo,
        link="https://x",
        local=None,
        imagem_url="https://img",
        destaque=False,
        data_evento=dia,
    )


def test_build_month_days_tem_todos_os_dias_do_mes():
    svc = IniciativaService(db=None, model=None)
    days = svc.build_month_days(date(2025, 2, 10))
    assert days[0] == date(2025, 2, 1) and days[-1] == date(2025, 2, 28)


def test_group_horarios_by_day_ordena_por_hora_e_titulo():
    svc = IniciativaService(db=None, model=None)
    dia = date(2025, 3, 5)
    rows = [
        _row("A", "h2", "Zeta", dia, dtime(9, 30), dtime(10, 0)),
        _row("A", "h1", "Alpha", dia, dtime(9, 30), dtime(10, 0)),
        _row("B", "h3", "Beta", dia, dtime(8, 0), dtime(9, 0)),
    ]
    tags = {
        "A": [TagSchema(id="t1", nome="Tech")],
        "B": [TagSchema(id="t2", nome="Edu")],
    }
    grouped = svc.group_horarios_by_day(rows, tags)
    assert [i.titulo for i in grouped[dia]] == ["Beta", "Alpha", "Zeta"]
