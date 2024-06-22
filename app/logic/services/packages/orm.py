import datetime
from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity, \
    PackageCalculationLog
from app.infra.cache.redis import RedisCacheDB
from app.infra.repositories.calculation.base import BaseCalculationLogRepository
from app.infra.repositories.packages.base import BasePackageRepository
from app.infra.repositories.packages import converters
from app.logic.services.packages.base import BasePackageService
from app.logic.utils import calculate_cost, get_rub_exchange_rates


@dataclass
class ORMPackageService(BasePackageService):
    repository: BasePackageRepository
    logs_repository: BaseCalculationLogRepository

    async def register_package(self, package: PackageEntity) -> PackageEntity:
        """
        Регистрирует новую посылку в системе.
        Args:
            package (PackageEntity): Объект посылки для регистрации.
        Returns:
            PackageEntity: Зарегистрированная посылка.
        """
        dto = converters.convert_package_entity_to_model(package)
        res_dto = await self.repository.add_package(dto)
        return res_dto.to_entity()

    async def calculate_delivery_cost(self) -> int:
        """
        Рассчитывает стоимость доставки для всех непосчитанных посылок.
        Returns:
            int: Количество посылок, для которых была рассчитана стоимость доставки.
        """
        exchange_rates = await get_rub_exchange_rates(RedisCacheDB())
        dollar_rate = exchange_rates['Valute']['USD']['Value']
        not_calculated = await self.repository.get_not_calculated_package_list()
        for package in not_calculated:
            delivery_cost = calculate_cost(package.price, package.weight, dollar_rate)
            package.delivery_cost = delivery_cost
            log = PackageCalculationLog(type_id=package.type_id, value=delivery_cost)
            await self.logs_repository.add_calculation_log(log)  # Добавляем лог в Mongo
        await self.repository.update_package_list_delivery_cost(not_calculated)
        return len(list(not_calculated))

    async def get_package_list(self, pagination, filters) -> Iterable[PackageEntity]:
        """
        Получает список посылок с учетом пагинации и фильтров.
        Args:
            pagination: Параметры пагинации.
            filters: Фильтры для поиска посылок.
        Returns:
            Iterable[PackageEntity]: Список посылок.
        """
        package_dto_list = await self.repository.get_package_list(pagination, filters)
        return [package_dto.to_entity() for package_dto in package_dto_list]

    async def get_package_count(self, filters) -> int:
        """
        Получает количество посылок, соответствующих заданным фильтрам.
        Args:
            filters: Фильтры для поиска посылок.
        Returns:
            int: Количество посылок.
        """
        return await self.repository.get_package_count(filters)

    async def get_package(self, package_id: int) -> PackageEntity:
        """
        Получает посылку по ее идентификатору.
        Args:
            package_id (int): Идентификатор посылки.
        Returns:
            PackageEntity: Найденная посылка.
        """
        dto = await self.repository.get_package(package_id)
        return dto.to_entity()

    async def get_package_types_list(self) -> Iterable[PackageTypeEntity]:
        """
        Получает список типов посылок.
        Returns:
            Iterable[PackageTypeEntity]: Список типов посылок.
        """
        type_dto_list = await self.repository.get_package_types_list()
        return [type_dto.to_entity() for type_dto in type_dto_list]

    async def add_package_type(self, p_type: PackageTypeEntity) -> PackageTypeEntity:
        """
        Добавляет новый тип посылки.
        Args:
            p_type (PackageTypeEntity): Объект типа посылки для добавления.
        Returns:
            PackageTypeEntity: Добавленный тип посылки.
        """
        type_dto = converters.convert_package_type_entity_to_model(p_type)
        res_dto = await self.repository.add_package_type(type_dto)
        return res_dto.to_entity()
