from dataclasses import dataclass

from redis.asyncio.client import Redis

from app.infra.cache.base import BaseCacheStorage
from app.settings.config import settings


@dataclass
class RedisCacheStorage(BaseCacheStorage):
    client: Redis = Redis()
    db_url: str = settings.redis.cache_url

    async def set_data(self, key, data, expiration):
        async with self.client.from_url(self.db_url) as client:
            await client.set(name=key, value=data, ex=expiration)

    async def get_data(self, key):
        async with self.client.from_url(self.db_url) as client:
            data = await client.get(key)
            return data
