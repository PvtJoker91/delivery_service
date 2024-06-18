from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.domain.values.packages import Title, PackageWeight, PackagePrice
from app.infra.models.base import TimedBaseModel

if TYPE_CHECKING:
    from app.infra.models.users import User


class PackageType(TimedBaseModel):
    __tablename__ = "package_types"

    name: Mapped[str] = mapped_column(String(100))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.name!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> PackageTypeEntity:
        return PackageTypeEntity(
            id=self.id,
            name=Title(self.name),
            created_at=self.created_at,
        )


class Package(TimedBaseModel):
    __tablename__ = "packages"

    title: Mapped[str] = mapped_column(String(100))
    weight: Mapped[float]
    price: Mapped[float]
    delivery_cost: Mapped[float | None]
    type_id: Mapped[int] = mapped_column(ForeignKey("package_types.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped['PackageType'] = relationship(back_populates="packages",)
    owner: Mapped['User'] = relationship(back_populates="packages",)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> PackageEntity:
        return PackageEntity(
            id=self.id,
            title=Title(self.title),
            weight=PackageWeight(self.weight),
            price=PackagePrice(self.price),
            delivery_cost=self.delivery_cost,
            type_id=self.type_id,
            owner_id=self.owner_id,
            type=self.type.to_entity(),
            owner=self.owner.to_entity(),
            created_at=self.created_at,
        )
