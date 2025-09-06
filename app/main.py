from fastapi import FastAPI

from app.routes.admin_route_example import router as admin_router_example
from app.routes.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Bah – Plataforma de Inovação de Caxias do Sul API",
    version="1.0.0",
    docs_url="/",
)

app.include_router(admin_router_example, prefix="/admin", tags=["admin"])
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bah – Plataforma de Inovação de Caxias do Sul"}
