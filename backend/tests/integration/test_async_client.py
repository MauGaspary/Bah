import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_public_route_responds_200(async_client):
    """Testa que rota pública responde 200 e middlewares executam"""
    async with async_client as client:
        response = await client.get("/")

        assert response.status_code == 307
        assert response.headers["location"] == "/docs"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_client_with_lifespan(async_client):
    """Testa que AsyncClient funciona com lifespan"""
    async with async_client as client:
        response1 = await client.get("/")
        response2 = await client.get("/docs")

        assert response1.status_code == 307
        assert response2.status_code == 200
