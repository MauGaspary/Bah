FROM python:3.12-slim
WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/cache/hf \
    SENTENCE_TRANSFORMERS_HOME=/opt/cache/hf \ 
    HF_HUB_DISABLE_TELEMETRY=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc-dev \
 && pip install --no-cache-dir pipenv \
 && rm -rf /var/lib/apt/lists/*

COPY Pipfile.lock Pipfile ./

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pipenv \
    pipenv install --dev --system --deploy --ignore-pipfile

RUN apt-get purge -y gcc libc-dev && apt-get autoremove -y

RUN --mount=type=cache,target=/opt/cache/hf python - <<'PY'
from sentence_transformers import SentenceTransformer
SentenceTransformer('intfloat/multilingual-e5-base', cache_folder='/opt/cache/hf')
PY

COPY . .

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]