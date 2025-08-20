from fastapi import FastAPI

from app.routes.admin_route_example import router as admin_router_example

app = FastAPI(title="Bah - Inovações API", version="1.0.0", docs_url="/")

app.include_router(admin_router_example, prefix="/admin", tags=["admin"])


@app.get("/")
def root():
    return {"message": "Bah - Inovações"}
