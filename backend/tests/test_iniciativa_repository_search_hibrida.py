import uuid

import pytest
from sqlalchemy import text

from app.models.descricoes_extras_model import DescricoesExtras
from app.models.iniciativa_model import MODEL_DIMENSION, Iniciativa
from app.models.iniciativa_tag_model import IniciativaTag
from app.models.organizador_model import Organizador
from app.models.tag_model import Tag
from app.models.usuario_model import Usuario
from app.repositories.iniciativa_repository import IniciativaRepository


def _nova_iniciativa(session, organizador_id, usuario_id, titulo, descricao, vetor):
    iniciativa = Iniciativa(
        titulo=titulo,
        descricao=descricao,
        organizador_id=organizador_id,
        link="https://example.com/evento",
        imagem_url="https://example.com/imagem.jpg",
        descricao_vetor=vetor,
        criado_por=usuario_id,
    )
    session.add(iniciativa)
    session.flush()
    return iniciativa


def _has_vector_extension(session) -> bool:
    result = session.execute(
        text("SELECT 1 FROM pg_type WHERE typname = 'vector' LIMIT 1")
    )
    return result.scalar() is not None


@pytest.fixture
def hybrid_search_dataset(db_session):
    if db_session.bind.dialect.name != "postgresql":
        pytest.skip("Requer Postgres para executar a busca vetorial")
    try:
        db_session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    except Exception:
        pass
    if not _has_vector_extension(db_session):
        pytest.skip("Extensão pgvector indisponível no ambiente de teste")

    repo = IniciativaRepository(db_session)

    usuario = Usuario(
        id=str(uuid.uuid4()),
        nome="Teste",
        sobrenome="Usuario",
        email="teste@example.com",
        senha_hash="hash",
    )
    organizador = Organizador(id=str(uuid.uuid4()), nome="Org Teste")
    tag_python = Tag(
        id=str(uuid.uuid4()), nome="Comunidade Python", descricao="Encontros mensais"
    )
    db_session.add_all([usuario, organizador, tag_python])
    db_session.flush()

    vetor_base = [0.0] * MODEL_DIMENSION

    iniciativa_titulo = _nova_iniciativa(
        db_session,
        organizador.id,
        usuario.id,
        "Imersão Python",
        "Conteúdo geral",
        vetor_base,
    )
    iniciativa_descricao = _nova_iniciativa(
        db_session,
        organizador.id,
        usuario.id,
        "Workshop de dados",
        "Sessão prática com python e pandas",
        vetor_base,
    )
    iniciativa_extras = _nova_iniciativa(
        db_session,
        organizador.id,
        usuario.id,
        "Networking Tech",
        "Conteúdo sobre comunicação",
        vetor_base,
    )
    db_session.add(
        DescricoesExtras(
            iniciativa_id=iniciativa_extras.id,
            descricao="Mentoria focada em python avançado",
            descricao_vetor=vetor_base,
        )
    )
    iniciativa_tag = _nova_iniciativa(
        db_session,
        organizador.id,
        usuario.id,
        "Comunidade de tecnologia",
        "Discussões abertas",
        vetor_base,
    )
    db_session.add(IniciativaTag(iniciativa_id=iniciativa_tag.id, tag_id=tag_python.id))
    iniciativa_neutra = _nova_iniciativa(
        db_session,
        organizador.id,
        usuario.id,
        "Feira de inovação",
        "Programação geral",
        vetor_base,
    )
    db_session.flush()

    embedding_consulta = [0.0] * MODEL_DIMENSION
    return {
        "repo": repo,
        "embedding": embedding_consulta,
        "iniciativas": {
            "titulo": iniciativa_titulo,
            "descricao": iniciativa_descricao,
            "extras": iniciativa_extras,
            "tag": iniciativa_tag,
            "neutra": iniciativa_neutra,
        },
    }


def test_search_hibrida_prioriza_reforco_lexico(hybrid_search_dataset):
    repo = hybrid_search_dataset["repo"]
    embedding_consulta = hybrid_search_dataset["embedding"]
    iniciativas = hybrid_search_dataset["iniciativas"]

    resultados, total = repo.search_hibrida(
        "python", embedding_consulta, page=1, size=10, min_score=0.0, rrf_k=60.0
    )

    assert total == 5
    titulos_ordenados = [item.titulo for item in resultados]

    assert titulos_ordenados[0] == iniciativas["titulo"].titulo
    assert titulos_ordenados[-1] == iniciativas["neutra"].titulo
    assert set(titulos_ordenados[:4]) == {
        iniciativas["titulo"].titulo,
        iniciativas["descricao"].titulo,
        iniciativas["extras"].titulo,
        iniciativas.get("tag").titulo,
    }


def test_search_hibrida_respeita_threshold(hybrid_search_dataset):
    repo = hybrid_search_dataset["repo"]
    embedding_consulta = hybrid_search_dataset["embedding"]
    iniciativas = hybrid_search_dataset["iniciativas"]

    resultados, total = repo.search_hibrida(
        "python", embedding_consulta, page=1, size=10, min_score=0.02, rrf_k=60.0
    )

    assert total == 4
    titulos = {item.titulo for item in resultados}
    assert iniciativas["neutra"].titulo not in titulos


def test_search_hibrida_threshold_garante_um_resultado(hybrid_search_dataset):
    repo = hybrid_search_dataset["repo"]
    embedding_consulta = hybrid_search_dataset["embedding"]
    iniciativas = hybrid_search_dataset["iniciativas"]

    resultados, total = repo.search_hibrida(
        "python", embedding_consulta, page=1, size=10, min_score=0.05, rrf_k=60.0
    )

    assert total == 1
    assert resultados[0].titulo in {
        iniciativas["titulo"].titulo,
        iniciativas["descricao"].titulo,
        iniciativas["extras"].titulo,
        iniciativas["tag"].titulo,
    }
