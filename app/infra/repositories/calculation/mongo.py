from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from motor.core import AgnosticClient

from app.domain.entities.packages import PackageCalculationLog
from app.infra.repositories.calculation.base import BaseCalculationLogRepository
from app.infra.repositories.calculation.converters import convert_log_entity_to_document
from app.settings.config import settings


@dataclass
class MongoCalculationLogRepository(BaseCalculationLogRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str = settings.mongo.mongo_initdb_database
    mongo_db_collection_name: str = settings.mongo.calculation_logs_collection_name

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def add_calculation_log(self, logs: Iterable[PackageCalculationLog]) -> None:
        await self._collection.insert_many([convert_log_entity_to_document(log) for log in logs])

    async def get_daily_calculation(self, log_date: date, package_type_id: int) -> (float, int):
        pipeline = [
            {
                "$match": {
                    "type_id": package_type_id,
                    "date": {
                        "$gte": log_date,
                        "$lte": log_date + timedelta(days=1)
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_value": {"$sum": "$value"},
                    "count": {"$sum": 1}
                }
            }
        ]

        result = await self._collection.aggregate(pipeline).to_list(length=1)

        if result:
            return result[0]["total_value"], result[0]["count"]
        return 0, 0
