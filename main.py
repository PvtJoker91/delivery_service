from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from app.api import router as api_router
from app.settings.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis = aioredis.from_url(settings.redis.cache_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, )
    app.include_router(router=api_router)

    return app
