from dataclasses import dataclass, field

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
    owner_id: int
    delivery_cost: float | None = None
    type: PackageType | None = None
    owner: User | None = None


@dataclass
class PackageFilter:
    type_id: int
    user_id: int
    is_calculated: bool
