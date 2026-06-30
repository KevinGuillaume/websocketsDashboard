import redis.asyncio as redis

pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379",
    decode_responses=True,
    socket_keepalive=True,    
    socket_connect_timeout=10,
    health_check_interval=30
)

def get_redis_client():
    return redis.Redis(connection_pool=pool)