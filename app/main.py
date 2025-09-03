from fastapi import FastAPI

from app.routes.admin_route_example import router as admin_router_example
from app.routes.auth_routes import router as auth_router

app = FastAPI(
    title="Bah – Plataforma de Inovação de Caxias do Sul API",
    version="1.0.0",
    docs_url="/",
)

app.include_router(admin_router_example, prefix="/admin", tags=["admin"])
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Bah – Plataforma de Inovação de Caxias do Sul"}
