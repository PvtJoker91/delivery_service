from dataclasses import dataclass

from app.logic.services.calculation_logs.base import BaseCalculationLogService
from app.logic.services.packages.base import BasePackageService


@dataclass
class CalculateDeliveryCostUseCase:
    package_service: BasePackageService
    log_service: BaseCalculationLogService

    async def execute(self) -> int:
        calculated_packages = await self.package_service.calculate_delivery_cost()
        await self.log_service.add_logs(calculated_packages)
        return len(list(calculated_packages))
