from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.packages import Package as PackageEntity
from app.infra.repositories.packages.base import BasePackageRepository


class SQLAlchemyPackageRepository(BasePackageRepository):
    session: AsyncSession

    async def add_package(self, package: PackageEntity):
        ...

    async def get_package(self, package_id: int):
        ...

    async def get_package_list(self, pagination, filters):
        ...

    async def get_package_types_list(self):
        ...
