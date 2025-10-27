import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config.settings import Settings
from app.middleware.auth_middleware import JWTMiddleware
from app.routes.admin_iniciativa_route import router as admin_iniciativa_router
from app.routes.auth_routes import router as auth_router
from app.routes.demo_route import router as demo_router
from app.routes.iniciativa_route import router as iniciativa_router
from app.routes.organizador_route import router as organizador_router
from app.routes.tag_route import router as tag_router
from app.routes.usuario_route import router as usuario_router
from app.utils.exception_handlers import domain_exception_handler, value_error_handler
from app.utils.exceptions import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings

    yield

    if settings.enable_database:
        from app.config.database import engine

        engine.dispose()


def create_app(settings=None):
    if settings is None:
        from app.config.settings import get_settings

        settings = get_settings()

    app = FastAPI(
        lifespan=lifespan,
        title="Bah – Plataforma de Inovação de Caxias do Sul API",
        version="1.0.0",
        docs_url="/docs",
        swagger_ui_parameters={
            "persistAuthorization": True,
        },
    )

    app.state.settings = settings

    if not os.getenv("TESTING", "false").lower() == "true":
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("intfloat/multilingual-e5-base")
        app.state.embedding_model = model
    else:
        app.state.embedding_model = None

    app.include_router(demo_router, prefix="/demo", tags=["demo"])
    app.include_router(
        admin_iniciativa_router, prefix="/admin/iniciativas", tags=["admin_iniciativas"]
    )
    app.include_router(
        organizador_router, prefix="/admin/organizadores", tags=["organizadores"]
    )
    app.include_router(tag_router, prefix="/admin/tags", tags=["tags"])
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(iniciativa_router, prefix="/iniciativas", tags=["iniciativas"])
    app.include_router(
        usuario_router, prefix="/admin/usuarios", tags=["admin_usuarios"]
    )

    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)

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
