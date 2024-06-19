from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.entities.packages import (Package as PackageEntity,
                                          PackageType as PackageTypeEntity,
                                          PackageFilter as PackageFilterEntity)
from app.infra.dtos.packages import PackageType, Package
from app.infra.dtos.users import User
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.packages.converters import convert_package_entity_to_model, \
    convert_package_type_entity_to_model
from app.logic.utils import is_nullable


@dataclass
class SQLAlchemyPackageRepository(BasePackageRepository):
    session: AsyncSession

    async def add_package(self, package: PackageEntity) -> PackageEntity:
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

    async def get_package(self, package_id: int) -> PackageEntity:
        async with self.session as session:
            stmt = select(Package).filter_by(id=package_id).options(
                joinedload(Package.type),
                joinedload(Package.owner),
            )
            try:
                res = await session.execute(stmt)
                package_dto = res.scalar_one()
                await session.commit()
            except Exception as e:
                raise Exception(f'хуйня с дб {e}')
            return package_dto.to_entity()

    async def get_package_list(self, pagination, filters: PackageFilterEntity) -> Iterable[PackageEntity]:
        async with self.session as session:
            query = select(Package).filter(
                Package.type_id == filters.type_id,
                Package.delivery_cost.isnot(is_nullable(filters.is_calculated))
            ).options(
                joinedload(Package.type),
                joinedload(Package.owner),
            ).limit(pagination.limit).offset(pagination.offset)
            try:
                res = await session.execute(query)
                package_dto_list = res.scalars().all()
            except Exception as e:
                raise Exception(f'хуйня с дб {e}')
            return [package_dto.to_entity() for package_dto in package_dto_list]

    async def get_package_count(self, filters: PackageFilterEntity) -> int:
        async with self.session as session:
            query = select(func.count(Package.id)).select_from(Package).filter(
                Package.type_id == filters.type_id,
                Package.delivery_cost.isnot(is_nullable(filters.is_calculated))
            )
            tasks_count = await session.execute(query)
            return tasks_count.scalar()

    async def add_package_type(self, p_type: PackageTypeEntity) -> PackageTypeEntity:
        async with self.session as session:
            type_dto = convert_package_type_entity_to_model(p_type)
            try:
                session.add(type_dto)
                await session.commit()
            except Exception as e:
                raise Exception('хуйня с type дб')
            return type_dto.to_entity()

    async def get_package_types_list(self) -> Iterable[PackageTypeEntity]:
        async with self.session as session:
            stmt = select(PackageType)
            try:
                res = await session.execute(stmt)
                type_list = res.scalars().all()
            except Exception as e:
                raise Exception('хуйня с type дб')
            return [type_dto.to_entity() for type_dto in type_list]
