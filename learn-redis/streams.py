import redis, time
r = redis.Redis(decode_responses=True)

# Add events
for user in ["alice", "bob", "carol"]:
    r.xadd("login_stream", {"user": user, "action": "login"})
print("✅ Added events to stream")

# Read all events
events = r.xrange("login_stream", "-", "+")
print("🧾 All events:")
for e_id, data in events:
    print(f"{e_id} => {data}")

# Read new events since a given ID
new_events = r.xread({"login_stream": "0-0"}, count=2)
print("\n📥 Read via xread:", new_events)
