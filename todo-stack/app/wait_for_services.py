# app/wait_for_services.py
import os
import time
import redis
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

def wait_for_db(retries=15, delay=1):
    engine = create_engine(DATABASE_URL)
    for i in range(retries):
        try:
            # Use text(...) so SQLAlchemy accepts the string
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Postgres is ready")
            return True
        except Exception as e:
            print(f"Postgres not ready, retry {i+1}/{retries} ({e})")
            time.sleep(delay)
    raise RuntimeError("Postgres not ready after retries")

def wait_for_redis(retries=15, delay=1):
    client = redis.from_url(REDIS_URL, decode_responses=True)
    for i in range(retries):
        try:
            client.ping()
            print("Redis is ready")
            return True
        except Exception as e:
            print(f"Redis not ready, retry {i+1}/{retries} ({e})")
            time.sleep(delay)
    raise RuntimeError("Redis not ready after retries")
