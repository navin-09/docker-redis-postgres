# app/wait_for_db.py
import time
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

def wait_for_db(retries=10, delay=1):
    engine = create_engine(DATABASE_URL)
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB is ready")
            return
        except Exception:
            print("Waiting for DB...")
            time.sleep(delay)
    raise RuntimeError("DB not ready")

if __name__ == "__main__":
    wait_for_db()
