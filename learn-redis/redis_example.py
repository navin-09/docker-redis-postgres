import redis
import random

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# String
r.set("greeting", "hello from python")
print("greeting:", r.get("greeting"))  # greeting: hello from python

# List
r.delete("tasks")
r.lpush("tasks", "t1", "t2")
print("tasks:", r.lrange("tasks", 0, -1))  # ['t2','t1']

# Hash
r.hset("user:1", mapping={"name":"Asha","score":50})
r.hset("user:2", mapping={"name":"Asha1","score":40})
r.hset("user:3", mapping={"name":"Asha2","score":60})
print("user:1:", r.hgetall("user:1"),r.hgetall("user:2"),r.hgetall("user:3"))

# Sorted set
r.zadd("board", {"alice":150, "bob":200})
print("top:", r.zrevrange("board", 0, 1, withscores=True))


# 1️⃣ Increment total login count
login_count = r.incr("logins")
print(f"Total logins so far: {login_count}")

# 2️⃣ Store user info in hash
user_id = "101"
r.hset(f"user:{user_id}", mapping={
    "name": "Asha",
    "email": "asha@example.com"
})
print("User profile:", r.hgetall(f"user:{user_id}"))

# 3️⃣ Add user to leaderboard (random score)
score = random.randint(100, 500)
r.zadd("top_users", {f"user:{user_id}": score})
print(f"Added user:{user_id} with score {score}")

# 4️⃣ Print top 3 users
top_users = r.zrevrange("top_users", 0, 2, withscores=True)
print("🏆 Top 3 Users:", top_users)