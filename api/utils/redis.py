import aioredis
from aioredis.client import PubSub

redis_pool = aioredis.from_url("redis://localhost")


def get_redis() -> aioredis.Redis:
    return redis_pool


def get_pubsub() -> PubSub:
    return redis_pool.pubsub()
