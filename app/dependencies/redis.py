from app.db.redis import get_redis

def get_redis_client():
    try:
        client = get_redis()
        yield client
    finally:
        client.close()
