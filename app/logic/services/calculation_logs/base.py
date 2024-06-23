from abc import abstractmethod, ABC
from datetime import datetime
from typing import Iterable

from app.domain.entities.packages import Package as PackageEntity, DailyCostCalculation


class BaseCalculationLogService(ABC):
    @abstractmethod
    async def add_logs(self, package_list: Iterable[PackageEntity]) -> None:
        ...

    @abstractmethod
    async def get_daily_calculation_log(self, package_type_id: int, date: datetime) -> DailyCostCalculation:
        ...
