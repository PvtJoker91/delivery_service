from abc import ABC, abstractmethod
from typing import Iterable

from app.infra.db.packages import Package, PackageType


class BasePackageRepository(ABC):
    @abstractmethod
    async def add_package(self, package: Package) -> Package:
        ...

    @abstractmethod
    async def update_package_list_delivery_cost(self, package_dto_list: Iterable[Package]) -> None:
        ...

    @abstractmethod
    async def get_not_calculated_package_list(self) -> Iterable[Package]:
        ...

    @abstractmethod
    async def get_package(self, package_id: int) -> Package:
        ...

    @abstractmethod
    async def get_package_list(self, pagination, filters) -> Iterable[Package]:
        ...

    @abstractmethod
    async def get_package_count(self, filters) -> int:
        ...

    @abstractmethod
    async def get_package_types_list(self) -> Iterable[PackageType]:
        ...

    @abstractmethod
    async def add_package_type(self, p_type: PackageType) -> PackageType:
        ...
