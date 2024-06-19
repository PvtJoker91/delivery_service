from dataclasses import dataclass

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.infra.repositories.packages.base import BasePackageRepository
from app.logic.services.packages.base import BasePackageService


@dataclass
class ORMPackageService(BasePackageService):
    repository: BasePackageRepository

    async def register_package(self, package: PackageEntity):
        return await self.repository.add_package(package)

    async def get_package_list(self, pagination, filters):
        ...

    async def get_package(self, package_id: int):
        ...

    async def get_package_types_list(self):
        ...

    async def add_package_type(self, p_type: PackageTypeEntity):
        return await self.repository.add_package_type(p_type)
