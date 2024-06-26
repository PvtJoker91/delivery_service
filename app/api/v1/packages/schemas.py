from datetime import datetime

from pydantic import BaseModel

from app.api.v1.users.schemas import UserSchema
from app.domain.constants import NOT_CALCULATED_COST_FIELD
from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity, \
    DailyCostCalculation
from app.domain.values.packages import Title, PackageWeight, PackagePrice


class PackageTypeSchema(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, p_type: PackageTypeEntity) -> 'PackageTypeSchema':
        return cls(name=p_type.name.as_generic_type(), id=p_type.id)


class PackageTypeCreateSchema(BaseModel):
    name: str

    def to_entity(self) -> PackageTypeEntity:
        return PackageTypeEntity(name=Title(self.name))


class RegisterPackageSchema(BaseModel):
    title: str
    weight: float
    price: float
    type_id: int

    def to_entity(self) -> PackageEntity:
        return PackageEntity(
            title=Title(self.title),
            weight=PackageWeight(self.weight),
            price=PackagePrice(self.price),
            type_id=self.type_id,
        )


class RegisterPackageResponseSchema(BaseModel):
    id: int
    title: str

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'RegisterPackageResponseSchema':
        return cls(title=package.title.as_generic_type(), id=package.id)


class PackageSchema(BaseModel):
    id: int
    title: str
    type_id: int

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageSchema':
        return cls(title=package.title.as_generic_type(), id=package.id, type_id=package.type_id)


class PackageDetailSchema(BaseModel):
    id: int
    title: str
    weight: float
    price: float
    type_id: int
    owner_id: int
    delivery_cost: str | float
    owner: UserSchema
    type: PackageTypeSchema

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageDetailSchema':
        return cls(
            id=package.id,
            title=package.title.as_generic_type(),
            weight=package.weight.as_generic_type(),
            price=package.price.as_generic_type(),
            delivery_cost=package.delivery_cost if package.delivery_cost else NOT_CALCULATED_COST_FIELD,
            owner_id=package.owner_id,
            type_id=package.type_id,
            owner=UserSchema.from_entity(package.owner),
            type=PackageTypeSchema.from_entity(package.type),
        )


class DailyCostCalculationSchema(BaseModel):
    type_id: int
    date: datetime
    packages_count: int
    total_cost: float

    @classmethod
    def from_entity(cls, log_entyty: DailyCostCalculation) -> 'DailyCostCalculationSchema':
        return cls(
            type_id=log_entyty.type_id,
            date=log_entyty.date,
            packages_count=log_entyty.packages_count,
            total_cost=log_entyty.total_cost,
        )
