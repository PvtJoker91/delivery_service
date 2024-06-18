from abc import ABC, abstractmethod
from app.domain.entities.packages import Package as PackageEntity


class BasePackageRepository(ABC):
    @abstractmethod
    async def add_package(self, package: PackageEntity):
        ...

    @abstractmethod
    async def get_package(self, oid: str):
        ...

    @abstractmethod
    async def get_package_list(self, pagination, filters):
        ...

    @abstractmethod
    async def get_package_types_list(self):
        ...
