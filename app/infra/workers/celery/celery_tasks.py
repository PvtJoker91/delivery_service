import asyncio

from app.infra.db.mongo_client import mongo_client
from app.infra.db.session import init_async_session
from app.infra.repositories.calculation.mongo import MongoCalculationLogRepository
from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.workers.celery.main import celery_app
from app.logic.services.calculation_logs.mongo import MongoCalculationLogService
from app.logic.services.packages.orm import ORMPackageService
from app.logic.use_cases.packages import CalculateDeliveryCostUseCase


@celery_app.task(name='cost_calculation')
def calculate_delivery_cost_task():
    async def run_task():
        package_service = ORMPackageService(
            SQLAlchemyPackageRepository(init_async_session())
        )
        log_service = MongoCalculationLogService(
            MongoCalculationLogRepository(mongo_client)
        )
        use_case = CalculateDeliveryCostUseCase(package_service, log_service)
        calculated = await use_case.execute()
        return f'Было рассчитано посылок - "{calculated}"'

    return asyncio.run(run_task())
