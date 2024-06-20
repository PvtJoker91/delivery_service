from celery import Celery
from celery.schedules import crontab

from app.domain.constants import PACKAGE_CALCULATE_SCHEDULE_MINUTES
from app.settings.config import settings


def init_worker() -> Celery:
    celery = Celery(
        broker=settings.redis.broker_url,
        backend=settings.redis.broker_url,
    )
    celery.autodiscover_tasks(['app.infra.workers.celery'], related_name='celery_tasks')
    celery.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
        beat_schedule={
            f'calculate-delivery-cost-every-{PACKAGE_CALCULATE_SCHEDULE_MINUTES}-minutes': {
                'task': 'app.infra.workers.celery.celery_tasks.calculate_delivery_cost_task',
                'schedule': crontab(minute=f'*/{PACKAGE_CALCULATE_SCHEDULE_MINUTES}'),
            },
        },
        beat_logfile='/logs/celery_beat.log',
    )
    return celery


celery_app = init_worker()
