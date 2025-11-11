import os
import redis
from flask import Flask

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")   # default to `redis`
r = redis.Redis(host=REDIS_HOST, port=6379)

@app.route('/')
def home():
    count = r.incr('hits')
    return f"🔁 This page has been visited {count} times!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
