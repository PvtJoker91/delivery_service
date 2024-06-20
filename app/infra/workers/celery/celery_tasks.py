import asyncio

from app.infra.db.session import init_async_session
from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.workers.celery.main import celery_app
from app.logic.services.packages.orm import ORMPackageService


@celery_app.task
def calculate_delivery_cost_task():
    async def run_task():
        session = init_async_session()
        service = ORMPackageService(SQLAlchemyPackageRepository(session))
        calculated = await service.calculate_delivery_cost()
        return f'Было рассчитано посылок - "{calculated}"'

    return asyncio.run(run_task())
