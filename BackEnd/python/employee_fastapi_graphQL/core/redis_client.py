import redis.asyncio as redis
import os

# localhost:6379, no password
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class RedisClient:
    def __init__(self, url: str):
        self.pool = redis.ConnectionPool.from_url(url, decode_responses=True)

    async def get_client(self):
        """
        Provides an asynchronous Redis client from the connection pool.
        """
        return redis.Redis.from_pool(self.pool)

# Singleton instance of the Redis client
redis_client = RedisClient(REDIS_URL)

async def get_redis_session():
    """
    Dependency injector for Redis client.
    """
    client = await redis_client.get_client()
    try:
        yield client
    finally:
        await client.close() # Ensure the connection is closed after use
