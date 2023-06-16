import aioredis
from aioredis.client import PubSub


class Redis:
    redis_pool = aioredis.from_url("redis://localhost")

    def get_redis(self) -> aioredis.Redis:
        return self.redis_pool

    def get_pubsub(self) -> PubSub:
        return self.redis_pool.pubsub()
