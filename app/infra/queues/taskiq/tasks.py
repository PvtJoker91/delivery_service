from app.domain.constants import PACKAGE_CALCULATE_SCHEDULE_MINUTES
from app.domain.exceptions.base import ApplicationException
from app.infra.cache.redis import RedisCacheStorage
from app.infra.db.mongo_client import mongo_client
from app.infra.db.session import init_async_session
from app.infra.repositories.calculation.mongo import MongoCalculationLogRepository
from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.queues.taskiq.broker import broker
from app.logging.factory import logger_factory
from app.logic.services.calculation_logs.mongo import MongoCalculationLogService
from app.logic.services.packages.orm import ORMPackageService
from app.logic.use_cases.packages import CalculateDeliveryCostUseCase


@broker.task(schedule=[{"cron": f"*/{PACKAGE_CALCULATE_SCHEDULE_MINUTES} * * * *", "args": [1]}])
async def calculate_delivery_cost_task(o):
    package_service = ORMPackageService(
        SQLAlchemyPackageRepository(init_async_session()),
        RedisCacheStorage()
    )
    log_service = MongoCalculationLogService(
        MongoCalculationLogRepository(mongo_client)
    )
    use_case = CalculateDeliveryCostUseCase(package_service, log_service)
    logger = logger_factory()
    try:
        calculated = await use_case.execute()
    except ApplicationException as e:
        logger.error(msg=f'Ошибка при выполнении отложенной задачи - "{e.message}"')
        raise e
    res = f'Задача завершена. Было рассчитано посылок - "{calculated}"'
    logger.info(msg=res)
    return res
