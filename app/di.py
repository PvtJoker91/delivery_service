import punq
from motor.core import AgnosticClient
from sqlalchemy.ext.asyncio import AsyncSession

from functools import lru_cache
from logging import Logger

from app.infra.cache.base import BaseCacheStorage
from app.infra.cache.redis import RedisCacheStorage
from app.infra.db.mongo_client import init_mongodb_client
from app.infra.db.session import init_async_session
from app.infra.repositories.calculation.base import BaseCalculationLogRepository
from app.infra.repositories.calculation.mongo import MongoCalculationLogRepository
from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.users.alchemy import SQLAlchemyUserRepository
from app.infra.repositories.users.base import BaseUserRepository
from app.logging.factory import logger_factory
from app.logic.services.calculation_logs.base import BaseCalculationLogService
from app.logic.services.calculation_logs.mongo import MongoCalculationLogService
from app.logic.services.packages.base import BasePackageService
from app.logic.services.packages.orm import ORMPackageService
from app.logic.services.users.base import BaseUserService
from app.logic.services.users.orm import ORMUserService
from app.logic.use_cases.packages import CalculateDeliveryCostUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # init internal stuff
    container.register(Logger, factory=logger_factory)

    # init session
    container.register(AsyncSession, factory=init_async_session)

    # init mongo
    container.register(AgnosticClient, factory=init_mongodb_client)

    # init repos
    container.register(BaseUserRepository)
    container.register(SQLAlchemyUserRepository)
    container.register(BasePackageRepository)
    container.register(SQLAlchemyPackageRepository)
    container.register(BaseCalculationLogRepository)
    container.register(MongoCalculationLogRepository)
    container.register(BaseCacheStorage)
    container.register(RedisCacheStorage)

    # init services
    def init_sqlalchemy_user_service():
        repository: BaseUserRepository = container.resolve(SQLAlchemyUserRepository)
        return ORMUserService(repository=repository)

    def init_sqlalchemy_package_service():
        repository: BasePackageRepository = container.resolve(SQLAlchemyPackageRepository)
        cache: BaseCacheStorage = container.resolve(RedisCacheStorage)
        return ORMPackageService(repository=repository, cache=cache)

    def init_mongo_calculation_logs_service():
        repository: BaseCalculationLogRepository = container.resolve(MongoCalculationLogRepository)
        return MongoCalculationLogService(repository=repository)

    container.register(BaseUserService, factory=init_sqlalchemy_user_service)
    container.register(BasePackageService, factory=init_sqlalchemy_package_service)
    container.register(BaseCalculationLogService, factory=init_mongo_calculation_logs_service)

    # init services

    container.register(CalculateDeliveryCostUseCase)

    return container
