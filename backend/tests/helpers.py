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
    if headers is None:
        headers = {}

    headers["Authorization"] = f"Bearer {token}"

    return request(
        client=client, method=method, path=path, json=json, headers=headers, **kwargs
    )
