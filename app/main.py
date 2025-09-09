from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config.settings import Settings
from app.middleware.auth_middleware import JWTMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.demo_route import router as demo_router
from app.routes.iniciativa_route import router as iniciativa_router


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
        docs_url="/docs",
    )

    app.state.settings = settings

    app.include_router(demo_router, prefix="/demo", tags=["demo"])
    app.include_router(
        iniciativa_router, prefix="/admin/iniciativas", tags=["admin", "iniciativas"]
    )
    app.include_router(auth_router)

    app.add_middleware(JWTMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return RedirectResponse(url="/docs")

    return app


app = create_app()
