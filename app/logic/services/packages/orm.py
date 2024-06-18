from app.domain.entities.packages import Package as PackageEntity
from app.logic.services.packages.base import BasePackageService


class ORMPackageService(BasePackageService):
    async def register_package(self, package: PackageEntity):
        ...

    async def get_package_list(self, pagination, filters):
        ...

    async def get_package(self, package_id: int):
        ...

    async def get_package_types_list(self):
        ...
