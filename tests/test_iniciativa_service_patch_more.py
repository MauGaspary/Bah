from types import SimpleNamespace

import app.services.iniciativa_service as mod
from app.schemas.iniciativa_schema import IniciativaPatchSchema
from app.services.iniciativa_service import IniciativaService


class M:
    def encode(self, *_a, **_k):
        return [1.0, 0.0, -1.0]


def test_patch_add_sem_modelo_erro():
    svc = IniciativaService(None, None)
    svc.repository = SimpleNamespace(update_partial=lambda **k: {"ok": True})
    p = IniciativaPatchSchema(descricoes_extras_add=["x"])
    try:
        svc.patch_iniciativa("i", p, editado_por="u", model=None)
        assert False, "esperava ValueError"
    except ValueError as e:
        assert "modelo de embedding" in str(e).lower()


def test_patch_add_e_update_com_modelo(monkeypatch):
    svc = IniciativaService(None, M())
    captured = {}

    def up(**k):
        captured.update(k)
        return {"id": "x"}

    svc.repository = SimpleNamespace(update_partial=up)
    monkeypatch.setattr(
        mod, "IniciativaSchema", SimpleNamespace(model_validate=lambda x: x)
    )
    p = IniciativaPatchSchema(
        descricoes_extras_add=["a", "b"],
        descricoes_extras_update=[{"id": "d1", "descricao": "novo"}],
    )
    out = svc.patch_iniciativa("I", p, editado_por="u", model=svc.model)
    assert out["id"] == "x"
    adds = captured["data"]["descricoes_extras_add"]
    upd = captured["data"]["descricoes_extras_update"][0]
    assert "descricao_vetor" in adds[0] and "descricao_vetor" in upd
