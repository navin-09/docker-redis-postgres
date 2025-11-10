# app/main.py
import os
import uuid
from flask import Flask, request, jsonify
from sqlalchemy import text
from .db import SessionLocal, engine, Base
from .models import Task
import redis
from .wait_for_services import wait_for_db, wait_for_redis

# Ensure env defaults
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_KEY = "tasks_count"

# Wait for services (helps avoid race conditions)
wait_for_db()
wait_for_redis()

# create tables (for simple demo; production: use Alembic migrations)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# initialize cached count if missing
def init_cache():
    if redis_client.get(CACHE_KEY) is None:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT COUNT(*) FROM tasks"))
            count = res.scalar()
        redis_client.set(CACHE_KEY, int(count or 0))

init_cache()

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title required"}), 400

    db = SessionLocal()
    try:
        task = Task(title=title)
        db.add(task)
        db.commit()
        db.refresh(task)
        # Increment cached count in Redis
        try:
            redis_client.incr(CACHE_KEY)
        except Exception:
            # best-effort cache update; if redis unavailable, ignore
            pass
        return jsonify({"id": str(task.id), "title": task.title, "done": task.done}), 201
    finally:
        db.close()

@app.route("/tasks", methods=["GET"])
def list_tasks():
    db = SessionLocal()
    try:
        rows = db.query(Task).order_by(Task.created_at.desc()).all()
        return jsonify([{"id": str(r.id), "title": r.title, "done": r.done, "created_at": r.created_at.isoformat()} for r in rows])
    finally:
        db.close()

@app.route("/tasks/count", methods=["GET"])
def tasks_count():
    # return cached count, with DB fallback
    cached = redis_client.get(CACHE_KEY)
    if cached is not None:
        return jsonify({"count_cached": int(cached)})
    # fallback to DB
    with engine.connect() as conn:
        res = conn.execute(text("SELECT COUNT(*) FROM tasks"))
        count = res.scalar()
    # set cache
    redis_client.set(CACHE_KEY, int(count or 0))
    return jsonify({"count_cached": int(count or 0)})

@app.route("/health")
def health():
    # basic health check for DB and Redis
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        redis_client.ping()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

if __name__ == "__main__":
    # Use port 8000 to avoid earlier conflict on 5000
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
