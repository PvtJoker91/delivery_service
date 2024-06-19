from abc import ABC, abstractmethod
from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity


class BasePackageRepository(ABC):
    @abstractmethod
    async def add_package(self, package: PackageEntity):
        ...

    @abstractmethod
    async def get_package(self, package_id: int):
        ...

    @abstractmethod
    async def get_package_list(self, pagination, filters):
        ...

    @abstractmethod
    async def get_package_types_list(self):
        ...

    @abstractmethod
    async def add_package_type(self, p_type: PackageTypeEntity):
        ...
