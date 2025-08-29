from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import Settings
from app.routes.admin_route_example import router as admin_router_example


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings

    print(
        f"Iniciando aplicação - Ambiente: {'TEST' if settings.testing else 'DEV' if settings.debug else 'PROD'}"
    )

    if settings.enable_database:
        print("Inicializando conexão com banco de dados...")

    if settings.enable_logging_setup:
        print(f"Configurando logging - Level: {settings.log_level}")

    print("Aplicação iniciada com sucesso!")

    yield

    print("Finalizando aplicação...")

    if settings.enable_database:
        print("Fechando conexões com banco de dados...")

    print("Aplicação finalizada!")


def create_app(settings=None):
    if settings is None:
        from app.config.settings import get_settings

        settings = get_settings()

    app = FastAPI(
        lifespan=lifespan,
        title="Bah – Plataforma de Inovação de Caxias do Sul API",
        version="1.0.0",
        docs_url="/",
    )

    app.state.settings = settings

    app.include_router(admin_router_example, prefix="/admin", tags=["admin"])

    @app.get("/")
    def root():
        return {"message": "Bah – Plataforma de Inovação de Caxias do Sul"}

    return app


app = create_app()
