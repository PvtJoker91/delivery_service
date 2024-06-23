from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import uuid4

from app.domain.entities.base import BaseEntity
from app.domain.entities.users import User
from app.domain.values.packages import PackageWeight, PackagePrice, Title


@dataclass
class PackageType(BaseEntity):
    name: Title


@dataclass
class Package(BaseEntity):
    title: Title
    weight: PackageWeight
    price: PackagePrice
    type_id: int
    owner_id: int | None = None
    delivery_cost: float | None = None
    type: PackageType | None = None
    owner: User | None = None


@dataclass
class PackageFilter:
    type_id: int
    user_id: int
    is_calculated: bool


@dataclass
class PackageCalculationLog:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    type_id: int
    value: float
    date: date = field(
        default_factory=datetime.today,
        kw_only=True
    )


@dataclass
class DailyCostCalculation:
    type_id: int
    date: datetime
    packages_count: int
    total_cost: float
