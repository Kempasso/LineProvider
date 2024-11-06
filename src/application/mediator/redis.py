from contextlib import asynccontextmanager

from redis.asyncio import Redis
from typing import Optional, Any

from src.config import server


class RedisClient:
    def __init__(self):
        self.redis = Redis(
            host=server.conf.redis.redis_host,
            port=server.conf.redis.redis_port,
            db=0
        )

    async def update_collection_element(
        self, collection_name: str, key: str, value: Any
    ):
        await self.redis.hset(collection_name, key=key, value=value)

    async def get_collection_element(
        self, collection_name: str, key: str
    ):
        return await self.redis.hget(collection_name, key=key)

    async def all_collection_elements(self, collection_name: str):
        return await self.redis.hgetall(collection_name)

    async def close(self):
        await self.redis.close()


async def get_redis_mediator():
    redis = None
    try:
        redis = RedisClient()
        yield redis
    except Exception as e:
        print(e)
    finally:
        if redis:
            await redis.close()


@asynccontextmanager
async def get_context_redis():
    async with get_redis_mediator() as redis:
        yield redis
