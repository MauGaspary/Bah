import importlib


def test_contato_model_import_sets_defaults():
    module = importlib.import_module("app.models.contato_model")
    contato_cls = getattr(module, "Contato")
    instance = contato_cls(
        nome="Nome",
        email="email@example.com",
        assunto="Assunto",
        mensagem="Mensagem",
    )

    assert instance.nome == "Nome"
    assert instance.email == "email@example.com"
