from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from app.domain.entities.packages import PackageCalculationLog


@dataclass
class BaseCalculationLogRepository(ABC):
    @abstractmethod
    async def add_calculation_log(self, log: PackageCalculationLog) -> None:
        ...

    @abstractmethod
    async def get_daily_calculation(self, log_date: date, package_type_id: int) -> float:
        ...

