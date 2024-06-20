import copy
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select, func, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.entities.packages import PackageFilter
from app.domain.exceptions.packages import (PackageTypeNotFoundException,
                                            PackageNotFoundException,
                                            PackageTypeAlreadyExistsException)
from app.domain.exceptions.users import UserNotFoundException
from app.infra.db.packages import PackageType, Package
from app.infra.db.session import init_async_session
from app.infra.db.users import User
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.packages.converters import convert_package_type_entity_to_model
from app.logic.utils import is_nullable


@dataclass
class SQLAlchemyPackageRepository(BasePackageRepository):
    session: AsyncSession

    """
    Репозиторий для управления посылками, использующий SQLAlchemy для работы с базой данных.
    Attributes:
        session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
    """

    async def add_package(self, package: Package) -> Package:
        """
        Добавляет новую посылку в базу данных.
        Args:
            package (Package): Объект посылки для добавления.
        Returns:
            Package: Добавленная посылка.
        Raises:
            UserNotFoundException: Если владелец посылки не найден.
            PackageTypeNotFoundException: Если тип посылки не найден.
        """
        async with self.session as session:
            package_dto = copy.deepcopy(package)
            user_stmt = select(User).filter_by(id=package_dto.owner_id)
            type_stmt = select(PackageType).filter_by(id=package_dto.type_id)
            try:
                user_res = await session.execute(user_stmt)
                user_dto = user_res.scalar_one()
            except NoResultFound:
                raise UserNotFoundException
            try:
                type_res = await session.execute(type_stmt)
                type_dto = type_res.scalar_one()
            except NoResultFound:
                raise PackageTypeNotFoundException
            package_dto.owner = user_dto
            package_dto.type = type_dto
            session.add(package_dto)
            await session.commit()
            return package_dto

    async def update_package_list_delivery_cost(self, package_dto_list: Iterable[Package]) -> None:
        """
        Обновляет стоимость доставки для списка посылок.
        Args:
            package_dto_list (Iterable[Package]): Список посылок для обновления.
        Raises:
            PackageNotFoundException: Если одна или несколько посылок не найдены.
        """
        async with self.session as session:
            try:
                for package in package_dto_list:
                    query = update(Package).filter_by(id=package.id).values(delivery_cost=package.delivery_cost)
                    await session.execute(query)
            except NoResultFound:
                raise PackageNotFoundException
            await session.commit()

    async def get_not_calculated_package_list(self) -> Iterable[Package]:
        """
        Получает список посылок, для которых не была рассчитана стоимость доставки.
        Returns:
            Iterable[Package]: Список посылок без рассчитанной стоимости доставки.
        Raises:
            PackageNotFoundException: Если посылки не найдены.
        """
        async with self.session as session:
            try:
                query = select(Package).filter(Package.delivery_cost.is_(None))
                res = await session.execute(query)
            except NoResultFound:
                raise PackageNotFoundException
            return res.scalars().all()

    async def get_package(self, package_id: int) -> Package:
        """
        Получает посылку по её идентификатору.
        Args:
            package_id (int): Идентификатор посылки.
        Returns:
            Package: Найденная посылка.
        Raises:
            PackageNotFoundException: Если посылка не найдена.
        """
        async with self.session as session:
            query = select(Package).filter_by(id=package_id).options(
                joinedload(Package.type),
                joinedload(Package.owner),
            )
            try:
                res = await session.execute(query)
                package_dto = res.scalar_one()
            except NoResultFound:
                raise PackageNotFoundException
            return package_dto

    async def get_package_list(self, pagination, filters: PackageFilter) -> Iterable[Package]:
        """
        Получает список посылок с учетом пагинации и фильтров.
        Args:
            pagination: Параметры пагинации.
            filters (PackageFilter): Фильтры для поиска посылок.
        Returns:
            Iterable[Package]: Список посылок.
        """
        async with self.session as session:
            query = select(Package).filter(
                Package.type_id == filters.type_id,
                Package.owner_id == filters.user_id,
                Package.delivery_cost.isnot(is_nullable(filters.is_calculated))
            ).options(
                joinedload(Package.type),
                joinedload(Package.owner),
            ).limit(pagination.limit).offset(pagination.offset)

            res = await session.execute(query)
            package_dto_list = res.scalars().all()

            return package_dto_list

    async def get_package_count(self, filters: PackageFilter) -> int:
        """
        Получает количество посылок, соответствующих заданным фильтрам.
        Args:
            filters (PackageFilter): Фильтры для поиска посылок.
        Returns:
            int: Количество посылок.
        """
        async with self.session as session:
            query = select(func.count(Package.id)).select_from(Package).filter(
                Package.type_id == filters.type_id,
                Package.delivery_cost.isnot(is_nullable(filters.is_calculated))
            )
            tasks_count = await session.execute(query)
            return tasks_count.scalar()

    async def add_package_type(self, p_type: PackageType) -> PackageType:
        """
        Добавляет новый тип посылки в базу данных.
        Args:
            p_type (PackageType): Объект типа посылки для добавления.
        Returns:
            PackageType: Добавленный тип посылки.
        Raises:
            PackageTypeAlreadyExistsException: Если тип посылки уже существует.
        """
        async with self.session as session:
            type_dto = convert_package_type_entity_to_model(p_type)
            try:
                session.add(type_dto)
                await session.commit()
            except IntegrityError:
                raise PackageTypeAlreadyExistsException
            return type_dto

    async def get_package_types_list(self) -> Iterable[PackageType]:
        """
        Получает список всех типов посылок.
        Returns:
            Iterable[PackageType]: Список типов посылок.
        """
        async with self.session as session:
            query = select(PackageType)
            res = await session.execute(query)
            type_dto_list = res.scalars().all()
            return type_dto_list
