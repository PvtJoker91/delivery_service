import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.api import router as api_router
from src.apps.tg_bot.main import init_tg_bot
from src.project.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis = aioredis.from_url(settings.redis.cache_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # await init_tg_bot()
    yield


origins = [
    "http://localhost:5173",
]

apm = make_apm_client({
    'SERVICE_NAME': settings.monitoring.service_name,
    'SECRET_TOKEN': settings.monitoring.apm_token,
    'SERVER_URL': settings.monitoring.apm_url,
    'ENVIRONMENT': 'dev',
})


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, )
    app.include_router(router=api_router)

    app.add_middleware(ElasticAPM, client=apm)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                       "Authorization"],
    )
    return app
