FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_ENV=demo \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data && \
    useradd --create-home --uid 10001 caiel && \
    chown -R caiel:caiel /app

USER caiel

EXPOSE 8000

CMD ["sh", "-c", "python scripts/init_db.py && uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"]
