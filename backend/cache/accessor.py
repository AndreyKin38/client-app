import redis


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host="localhost",
        port=6379,
        db=0
    )


def set_value():
    conn = get_redis_connection()
    conn.set('value', 1)


