from dataclasses import dataclass

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
    type_oid: str
    type: PackageType
    user_oid: str
    owner: User
    delivery_cost: str | float
