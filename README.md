# Bah – Plataforma de Inovação de Caxias do Sul


# Desenvolvimento Local

```
# Instalar dependências
pip install pipenv
pipenv install --dev

# Configurar pre-commit hooks
pipenv run pre-commit install
```

# Rodar aplicação
```
pipenv run app
```

# Testes
```
pipenv run test
pipenv run test:cov
```

# Qualidade de código
```
pipenv run precommit
pipenv run format:all
pipenv run lint:all
pipenv run pylint:all
```


# Docker

# Rodar aplicação
```
docker compose up --build
```

# Testes no Docker
```
docker compose exec app pytest tests --cov=app
```

# Ferramentas de qualidade no Docker
```
docker compose exec app black .
docker compose exec app pylint app
docker compose exec app pre-commit run --all-files
```

# Parar aplicação
```
docker compose down
```
