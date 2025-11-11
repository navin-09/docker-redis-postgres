from flask import Flask
import redis, os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def home():
    count = r.incr('hits')
    return f"🔁 Connected to Redis at {redis_host}:{redis_port} — Page visited {count} times!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

