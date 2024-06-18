from pydantic import BaseModel

from app.api.v1.users.schemas import UserSchema
from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.domain.values.packages import Title, PackageWeight, PackagePrice


class PackageTypeSchema(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, p_type: PackageTypeEntity) -> 'PackageTypeSchema':
        return cls(name=p_type.name.as_generic_type(), id=p_type.id)


class RegisterPackageSchema(BaseModel):
    title: str
    weight: float
    price: float
    type_id: str
    owner_id: str

    def to_entity(self):
        return PackageEntity(
            title=Title(self.title),
            weight=PackageWeight(self.weight),
            price=PackagePrice(self.price),
            type_id=self.type_id,
            owner_id=self.owner_id,
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
    type_id: str

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageSchema':
        return cls(title=package.title.as_generic_type(), id=package.id, type_id=package.type_id)


class PackageDetailSchema(BaseModel):
    id: int
    title: str
    weight: float
    price: float
    type_id: str
    owner_id: str
    delivery_cost: str | float
    owner: UserSchema
    type: PackageTypeSchema

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageDetailSchema':
        return cls(title=package.title.as_generic_type(), id=package.id, type_id=package.type_id)
