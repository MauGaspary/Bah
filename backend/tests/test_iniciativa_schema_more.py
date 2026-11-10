from datetime import date, time, timedelta

import pytest

from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaHorarioPatch


def _pick_tipo_valido() -> str:
    try:
        schema = IniciativaCreate.model_json_schema()
        tipo_node = (
            schema.get("properties", {})
            .get("horarios", {})
            .get("items", {})
            .get("properties", {})
            .get("tipo", {})
        )
        enum_vals = tipo_node.get("enum")
        if enum_vals and isinstance(enum_vals, list):
            return enum_vals[0]
    except Exception:
        pass
    return "presencial"


TIPO_VALIDO = _pick_tipo_valido()

BASE_TOP = {
    "link": "https://example.com",
    "imagem_url": "https://example.com/img.png",
}

BASE_HORARIO = {
    "data_evento": "2099-12-31",
    "hora_inicio": "09:00",
    "hora_fim": "10:00",
    "tipo": TIPO_VALIDO,
}


def test_iniciativa_schema_normaliza_campos_e_aceita_payload_minimo_valido():
    payload = {
        "titulo": "  Cobertura  ",
        "descricao": " ok ",
        "local": "  POA ",
        "organizador_id": "00000000-0000-0000-0000-000000000000",
        "horarios": [BASE_HORARIO],
        "tags_ids": ["A", "B"],
        **BASE_TOP,
    }
    model = IniciativaCreate(**payload)

    assert isinstance(model.titulo, str)
    assert model.titulo.strip() == "Cobertura"
    assert model.local.strip() == "POA"

    assert model.horarios
    h = model.horarios[0]
    assert h.data_evento.isoformat() == "2099-12-31"
    assert str(h.hora_inicio) == "09:00:00"
    assert str(h.hora_fim) == "10:00:00"
    assert getattr(h, "tipo") == h.tipo


def test_iniciativa_schema_campos_ja_limpos_passam_direto():
    payload = {
        "titulo": "Cobertura",
        "descricao": "ok",
        "local": "POA",
        "organizador_id": "00000000-0000-0000-0000-000000000000",
        "horarios": [BASE_HORARIO],
        "tags_ids": [],
        **BASE_TOP,
    }
    model = IniciativaCreate(**payload)
    assert model.titulo == "Cobertura"
    assert model.local == "POA"
    assert len(model.horarios) == 1


def test_horario_patch_valida_ordem_horarios():
    with pytest.raises(ValueError):
        IniciativaHorarioPatch(
            hora_inicio=time(10, 0),
            hora_fim=time(9, 0),
        )


def test_horario_patch_valida_data_nao_retroativa():
    yesterday = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        IniciativaHorarioPatch(data_evento=yesterday)


def test_horario_patch_valido_retorna_valores():
    patch = IniciativaHorarioPatch(
        hora_inicio=time(9, 0),
        hora_fim=time(10, 0),
        data_evento=date.today(),
    )
    assert patch.hora_fim == time(10, 0)
    assert patch.data_evento == date.today()
