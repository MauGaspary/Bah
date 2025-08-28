from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.admin_route_example import router as admin_router_example


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação")
    yield
    print("Finalizando aplicação")


app = FastAPI(
    lifespan=lifespan,
    title="Bah – Plataforma de Inovação de Caxias do Sul API",
    version="1.0.0",
    docs_url="/",
)

app.include_router(admin_router_example, prefix="/admin", tags=["admin"])


@app.get("/")
def root():
    return {"message": "Bah – Plataforma de Inovação de Caxias do Sul"}


def create_app():
    return app
