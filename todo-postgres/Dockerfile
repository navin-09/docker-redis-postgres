# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# system deps for psycopg2; slim needs these
RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV FLASK_APP=app.main
EXPOSE 5000

CMD ["python", "-u", "-m", "app.main"]
