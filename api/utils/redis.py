import redis.asyncio as redis
from redis.asyncio.client import PubSub

redis_pool = redis.from_url("redis://localhost")


def get_redis() -> redis.Redis:
    return redis_pool


def get_pubsub() -> PubSub:
    return redis_pool.pubsub()
