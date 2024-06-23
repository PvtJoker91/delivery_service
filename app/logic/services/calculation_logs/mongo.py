from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from app.domain.entities.packages import Package as PackageEntity, PackageCalculationLog, DailyCostCalculation

from app.infra.repositories.calculation.base import BaseCalculationLogRepository
from app.logic.services.calculation_logs.base import BaseCalculationLogService


@dataclass
class MongoCalculationLogService(BaseCalculationLogService):
    repository: BaseCalculationLogRepository

    async def add_logs(self, package_list: Iterable[PackageEntity]) -> None:
        logs = []
        for package in package_list:
            logs.append(PackageCalculationLog(type_id=package.type_id, value=package.delivery_cost))
        if logs:
            await self.repository.add_calculation_log(logs)

    async def get_daily_calculation_log(self, date: datetime, package_type_id: int) -> DailyCostCalculation:
        value, count = await self.repository.get_daily_calculation(log_date=date, package_type_id=package_type_id)
        return DailyCostCalculation(type_id=package_type_id, date=date, total_cost=value, packages_count=count)
