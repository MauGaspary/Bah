"""Helpers para testes - padronização de requests"""

from typing import Any, Dict, Optional

from fastapi.testclient import TestClient


def request(
    client: TestClient,
    method: str,
    path: str,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    **kwargs,
):
    """
    Helper para requests padronizados.

    Args:
        client: TestClient do FastAPI
        method: Método HTTP (GET, POST, PUT, DELETE, etc.)
        path: Caminho da API
        json: Dados JSON para o body
        headers: Headers customizados
        **kwargs: Argumentos adicionais para o request

    Returns:
        Response object
    """
    # Padronizar Content-Type quando há body
    if json is not None:
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")

    return client.request(
        method=method.upper(), url=path, json=json, headers=headers, **kwargs
    )


def request_auth(
    client: TestClient,
    method: str,
    path: str,
    token: str,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    **kwargs,
):
    """
    Helper para requests autenticados.

    Args:
        client: TestClient do FastAPI
        method: Método HTTP (GET, POST, PUT, DELETE, etc.)
        path: Caminho da API
        token: Token de autenticação
        json: Dados JSON para o body
        headers: Headers customizados
        **kwargs: Argumentos adicionais para o request

    Returns:
        Response object
    """
    if headers is None:
        headers = {}

    # Injetar Authorization Bearer
    headers["Authorization"] = f"Bearer {token}"

    return request(
        client=client, method=method, path=path, json=json, headers=headers, **kwargs
    )
