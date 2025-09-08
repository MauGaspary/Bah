# Guia de Testes

## Comandos

```bash
# Executar testes
pipenv run test
pipenv run test:cov  # com coverage

# Docker
docker compose run --rm test
docker compose run --rm test-cov # com coverage
```

## Helpers de Teste

### request(client, method, path, json=None, headers=None, **kw)

Para requests básicos, padroniza Content-Type automaticamente:

```python
from tests.helpers import request

# GET simples
response = request(client, "GET", "/admin/")

# POST com JSON (Content-Type automático)
response = request(client, "POST", "/admin/", json={
    "username": "test",
    "email": "test@example.com"
})
```

### request_auth(client, method, path, token, **kw)

Para requests autenticados, injeta Authorization Bearer:

```python
from tests.helpers import request_auth

response = request_auth(client, "GET", "/admin/protected", token="jwt-token")
```

Ambos helpers eliminam boilerplate e mantêm código consistente.
