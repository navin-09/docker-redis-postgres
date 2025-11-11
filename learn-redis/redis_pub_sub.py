import redis
import threading
import time

# r = redis.Redis(decode_responses=True)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("chatroom")
    print("Subscribed to 'chatroom'...")

    for msg in pubsub.listen():
        print(msg)
        if msg["type"] == "message":
            print("📩 Received:", msg["data"])

# Run subscriber in a thread
threading.Thread(target=subscriber, daemon=True).start()

time.sleep(1)
r.publish("chatroom", "Hey from Python!")
time.sleep(2)
