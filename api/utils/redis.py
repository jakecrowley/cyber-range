import aioredis

redis_pool = aioredis.from_url("redis://localhost")


async def get_redis() -> aioredis.Redis:
    return redis_pool
