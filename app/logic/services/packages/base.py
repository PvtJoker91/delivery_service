from abc import ABC, abstractmethod
from typing import Iterable

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity


class BasePackageService(ABC):

    @abstractmethod
    async def register_package(self, package: PackageEntity) -> PackageEntity:
        ...

    @abstractmethod
    async def get_package_list(self, pagination, filters) -> Iterable[PackageEntity]:
        ...

    @abstractmethod
    async def get_package_count(self, filters) -> int:
        ...

    @abstractmethod
    async def get_package(self, package_id: int) -> PackageEntity:
        ...

    @abstractmethod
    async def get_package_types_list(self) -> Iterable[PackageTypeEntity]:
        ...

    @abstractmethod
    async def add_package_type(self, p_type: PackageTypeEntity) -> PackageTypeEntity:
        ...
