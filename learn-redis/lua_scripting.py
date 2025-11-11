import redis
script = """
local val = redis.call('GET', KEYS[1])
if not val then
  return 0
end
return tonumber(val) + 1
"""
r = redis.Redis(decode_responses=True)
result = r.eval(script, 1, "counter")
print("Result:", result)
