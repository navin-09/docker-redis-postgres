# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# system deps for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "-u", "-m", "app.main"]
