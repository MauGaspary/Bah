FROM python:3.12-slim

WORKDIR /app

RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile* ./

RUN pipenv install --dev --system --deploy

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]