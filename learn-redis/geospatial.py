# geospatial_fixed.py
import redis
from redis.exceptions import DataError, RedisError

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("redis-py version:", redis.__version__)

# prepare data (lon, lat, name)
places = [
    (77.5946, 12.9716, "Bangalore"),
    (80.2707, 13.0827, "Chennai"),
    (72.8777, 19.0760, "Mumbai"),
    (88.3639, 22.5726, "Kolkata"),
]

# clear existing key
r.delete("cities")


# Verify whether keys were added; if not, attempt fallback
if r.zcard("cities") == 0:
    # Build flat args: key lon lat member lon lat member ...
    flat_args = []
    for lon, lat, name in places:
        flat_args.extend([lon, lat, name])

    # redis-py execute_command requires strings/numbers in args
    try:
        # Note: command signature is: GEOADD key lon lat member [lon lat member ...]
        r.execute_command("GEOADD", "cities", *flat_args)
        print("geoadd via execute_command succeeded")
    except Exception as e:
        print("Fallback execute_command also failed:", type(e), e)
        raise

# Show results
try:
    dist = r.geodist("cities", "Bangalore", "Chennai", unit="km")
    print(f"Distance Bangalore ↔ Chennai: {float(dist):.2f} km")
    nearby = r.georadius("cities", 77.6, 12.9, 400, unit="km")
    print("Nearby cities (within 400 km):", nearby)
except Exception as e:
    print("Error while querying geo data:", type(e), e)
    raise
