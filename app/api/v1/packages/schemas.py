from pydantic import BaseModel

from app.api.v1.users.schemas import UserSchema
from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.domain.values.packages import Title, PackageWeight, PackagePrice


class PackageTypeSchema(BaseModel):
    oid: str
    name: str

    @classmethod
    def from_entity(cls, p_type: PackageTypeEntity) -> 'PackageTypeSchema':
        return cls(name=p_type.name.as_generic_type(), oid=p_type.oid)


class RegisterPackageSchema(BaseModel):
    title: str
    weight: float
    price: float
    type_oid: str
    owner_oid: str

    def to_entity(self):
        return PackageEntity(
            title=Title(self.title),
            weight=PackageWeight(self.weight),
            price=PackagePrice(self.price),
            type_oid=self.type_oid,
            owner_oid=self.owner_oid,
        )


class RegisterPackageResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'RegisterPackageResponseSchema':
        return cls(title=package.title.as_generic_type(), oid=package.oid)


class PackageSchema(BaseModel):
    oid: str
    title: str
    type_oid: str

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageSchema':
        return cls(title=package.title.as_generic_type(), oid=package.oid, type_oid=package.type_oid)


class PackageDetailSchema(BaseModel):
    oid: str
    title: str
    weight: float
    price: float
    type_oid: str
    owner_oid: str
    delivery_cost: str | float
    owner: UserSchema
    type: PackageTypeSchema

    @classmethod
    def from_entity(cls, package: PackageEntity) -> 'PackageDetailSchema':
        return cls(title=package.title.as_generic_type(), oid=package.oid, type_oid=package.type_oid)
