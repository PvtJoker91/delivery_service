from logging import Logger, getLogger

from punq import Container

from app.di import _initialize_container
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.packages.memory import MemoryPackageRepository
from app.infra.repositories.users.base import BaseUserRepository
from app.infra.repositories.users.memory import MemoryUserRepository
from app.logic.services.packages.base import BasePackageService
from app.logic.services.packages.orm import ORMPackageService
from app.logic.services.users.base import BaseUserService
from app.logic.services.users.orm import ORMUserService


def init_dummy_container() -> Container:
    container = _initialize_container()

    container.register(Logger, factory=getLogger)

    container.register(MemoryUserRepository)
    container.register(MemoryPackageRepository)
    container.register(BaseUserRepository, MemoryUserRepository)
    container.register(BasePackageRepository, MemoryPackageRepository)

    def init_memory_user_service():
        repository: BaseUserRepository = container.resolve(MemoryUserRepository)
        return ORMUserService(repository=repository)

    def init_memory_task_service():
        repository: BasePackageRepository = container.resolve(MemoryPackageRepository)
        return ORMPackageService(repository=repository)

    container.register(BaseUserService, factory=init_memory_user_service)
    container.register(BasePackageService, factory=init_memory_task_service)

    return container
