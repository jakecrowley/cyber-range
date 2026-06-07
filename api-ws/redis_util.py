import redis.asyncio as redis
from redis.asyncio.client import PubSub


class Redis:
    redis_pool = redis.from_url("redis://localhost")

    def get_redis(self) -> redis.Redis:
        return self.redis_pool

    def get_pubsub(self) -> PubSub:
        return self.redis_pool.pubsub()
