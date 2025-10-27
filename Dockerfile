FROM python:3.12-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/cache/hf \
    SENTENCE_TRANSFORMERS_HOME=/opt/cache/hf \
    HF_HUB_DISABLE_TELEMETRY=1 \
    PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

# Copiar arquivos de dependências
COPY Pipfile.lock Pipfile ./

# Instalar dependências Python (incluindo dev)
RUN pipenv install --dev --system --deploy --ignore-pipfile

# Baixar modelo sentence-transformers no build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-base', cache_folder='/opt/cache/hf')"

# Remover gcc para reduzir tamanho da imagem
RUN apt-get purge -y gcc libc-dev && apt-get autoremove -y

# Copiar código da aplicação
COPY . .

EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
