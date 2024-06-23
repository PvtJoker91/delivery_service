from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.settings.config import settings


broker = ListQueueBroker(
    url=settings.redis.broker_url,
).with_result_backend(RedisAsyncResultBackend(settings.redis.broker_url))

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
