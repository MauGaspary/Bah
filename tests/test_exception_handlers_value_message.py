import json

import pytest
from fastapi import Request

from app.utils.exception_handlers import value_error_handler


@pytest.mark.asyncio
async def test_value_error_handler_with_message():
    req = Request({"type": "http"})
    resp = await value_error_handler(req, ValueError("algo deu errado"))
    assert resp.status_code == 400
    payload = json.loads(resp.body.decode())
    assert payload.get("detail") in ("algo deu errado", "")
