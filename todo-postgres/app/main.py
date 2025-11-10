# app/main.py
import os
import uuid
from flask import Flask, request, jsonify
from sqlalchemy import text
from .db import SessionLocal, engine, Base
from .models import Task

# initialize DB tables (simple approach for learning)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    db = SessionLocal()
    try:
        task = Task(title=title)
        db.add(task)
        db.commit()
        db.refresh(task)
        return jsonify({"id": str(task.id), "title": task.title, "done": task.done}), 201
    finally:
        db.close()

@app.route("/tasks", methods=["GET"])
def list_tasks():
    db = SessionLocal()
    try:
        rows = db.query(Task).order_by(Task.created_at.desc()).all()
        if not rows:
            return jsonify({"message": "no tasks found", "tasks": []})
        return jsonify(
            [
                {
                    "id": str(r.id),
                    "title": r.title,
                    "done": r.done,
                    "created_at": r.created_at.isoformat(),
                }
                for r in rows
            ]
        )
    finally:
        db.close()

@app.route("/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    db = SessionLocal()
    try:
        task = db.get(Task, uuid.UUID(task_id))
        if not task:
            return jsonify({"error": "not found"}), 404
        # toggle done
        task.done = not task.done
        db.commit()
        db.refresh(task)
        return jsonify({"id": str(task.id), "done": task.done})
    finally:
        db.close()

@app.route("/health")
def health():
    # simple health check
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
