import redis
from app.core.config import Config

if not Config.REDIS_URL:
    raise ValueError("No REDIS_URL provided. Set REDIS_URL environment variable.")

def get_redis():
    return redis.Redis.from_url(Config.REDIS_URL)
