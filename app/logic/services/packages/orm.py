from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.infra.repositories.packages.base import BasePackageRepository
from app.logic.services.packages.base import BasePackageService


@dataclass
class ORMPackageService(BasePackageService):
    repository: BasePackageRepository

    async def register_package(self, package: PackageEntity) -> PackageEntity:
        return await self.repository.add_package(package)

    async def get_package_list(self, pagination, filters) -> Iterable[PackageEntity]:
        return await self.repository.get_package_list(pagination, filters)

    async def get_package_count(self, filters) -> int:
        return await self.repository.get_package_count(filters)

    async def get_package(self, package_id: int) -> PackageEntity:
        return await self.repository.get_package(package_id)

    async def get_package_types_list(self) -> Iterable[PackageTypeEntity]:
        return await self.repository.get_package_types_list()

    async def add_package_type(self, p_type: PackageTypeEntity) -> PackageTypeEntity:
        return await self.repository.add_package_type(p_type)
