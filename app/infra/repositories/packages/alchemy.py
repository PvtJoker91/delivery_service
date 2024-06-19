from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.infra.dtos.packages import PackageType
from app.infra.dtos.users import User
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.packages.converters import convert_package_entity_to_model, \
    convert_package_type_entity_to_model


@dataclass
class SQLAlchemyPackageRepository(BasePackageRepository):
    session: AsyncSession

    async def add_package(self, package: PackageEntity):
        async with self.session as session:
            package_dto = convert_package_entity_to_model(package)
            user_stmt = select(User).filter_by(id=package_dto.owner_id)
            type_stmt = select(PackageType).filter_by(id=package_dto.type_id)
            try:
                user_res = await session.execute(user_stmt)
                type_res = await session.execute(type_stmt)
                user_dto = user_res.scalar_one()
                type_dto = type_res.scalar_one()
                package_dto.owner = user_dto
                package_dto.type = type_dto
                session.add(package_dto)
                await session.commit()
            except Exception as e:
                raise Exception(f'хуйня с дб {e}')
            return package_dto.to_entity()

    async def get_package(self, package_id: int):
        ...

    async def get_package_list(self, pagination, filters):
        ...

    async def add_package_type(self, p_type: PackageTypeEntity):
        async with self.session as session:
            type_dto = convert_package_type_entity_to_model(p_type)
            try:
                session.add(type_dto)
                await session.commit()
            except Exception as e:
                raise Exception('хуйня с type дб')
            return type_dto.to_entity()

    async def get_package_types_list(self):
        ...
