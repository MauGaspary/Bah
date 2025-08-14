# Innovation Search API com IA


# Instalar dependências local

É preciso ter o python e o pip instalado

```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

# Rodar aplicação
```
uvicorn app.main:app --reload
```


# Comando de teste
```
pytest tests/test_admin_example.py -v
```


# Docker

## Rodar com Docker Compose
```
docker compose up --build
ou
docker compose up --build -d
```

## Parar e remover containers
```
docker compose down  
````

## Rodar apenas o app
```
docker build -t bah-backend .
docker run -p 8000:8000 bah-backend
```





# Migrations

## Gerar nova migration
```
alembic revision --autogenerate -m "description"
```

## Aplicar migrations
```
alembic upgrade head
```

## Reverter migration
```
alembic downgrade -1
```
