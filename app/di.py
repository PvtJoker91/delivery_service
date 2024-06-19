import punq
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from functools import lru_cache
from logging import Logger, getLogger

from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.users.alchemy import SQLAlchemyUserRepository
from app.infra.repositories.users.base import BaseUserRepository
from app.logic.services.packages.base import BasePackageService
from app.logic.services.packages.orm import ORMPackageService
from app.logic.services.users.base import BaseUserService
from app.logic.services.users.orm import ORMUserService
from app.settings.config import settings


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # init internal stuff
    container.register(Logger, factory=getLogger)

    # init session
    def init_async_session():
        engine = create_async_engine(url=settings.db.db_url, echo=settings.db.echo,)
        session_factory = async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        return session_factory()

    container.register(AsyncSession, factory=init_async_session)

    # init repos

    container.register(BaseUserRepository)
    container.register(SQLAlchemyUserRepository)
    container.register(BasePackageRepository)
    container.register(SQLAlchemyPackageRepository)

    # initialize services
    def init_sqlalchemy_user_service():
        repository: BaseUserRepository = container.resolve(SQLAlchemyUserRepository)
        return ORMUserService(repository=repository)

    def init_sqlalchemy_package_service():
        repository: BasePackageRepository = container.resolve(SQLAlchemyPackageRepository)
        return ORMPackageService(repository=repository)

    container.register(BaseUserService, factory=init_sqlalchemy_user_service)
    container.register(BasePackageService, factory=init_sqlalchemy_package_service)

    return container
