import json

import pytest
from fastapi import Request

from app.utils.exception_handlers import domain_exception_handler, value_error_handler
from app.utils.exceptions import DomainException


@pytest.mark.asyncio
async def test_value_error_handler_default_message_when_no_msg():

    req = Request({"type": "http"})
    resp = await value_error_handler(req, ValueError())

    assert resp.status_code == 400

    payload = json.loads(resp.body.decode())

    assert isinstance(payload.get("detail"), str)

    assert payload["detail"] in ("", "Requisição inválida")


class CustomDomainException(DomainException):
    pass


@pytest.mark.asyncio
async def test_domain_exception_handler_default_branch():
    req = Request({"type": "http"})
    resp = await domain_exception_handler(req, CustomDomainException("erro"))
    assert resp.status_code == 400
    payload = json.loads(resp.body.decode())
    assert payload["detail"] == "erro"
