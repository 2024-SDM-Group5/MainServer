import time

def get_redis_key(lat, lng):
    """Generate a Redis key based on rounded latitude and longitude."""
    return f"query:{round(lat, 2)}:{round(lng, 2)}"

def need_query_position(redis, lat, lng):
    """Check if the coordinates have been queried in the last hour."""
    key = get_redis_key(lat, lng)
    last_queried = redis.get(key)
    if last_queried is None or (time.time() - float(last_queried)) > 86400:
        redis.set(key, time.time())
        return True
    return False

def need_query_place(redis, place_id):
    """Check if the place has been queried in the last hour."""
    key = f"query:{place_id}"
    last_queried = redis.get(key)
    if last_queried is None or (time.time() - float(last_queried)) > 86400:
        redis.set(key, time.time())
        return True
    return False