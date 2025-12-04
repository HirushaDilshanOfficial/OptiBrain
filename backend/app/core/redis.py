import redis.asyncio as redis
from app.core.config import settings

async def get_redis_pool():
    return redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
