from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.users import User as UserEntity
from app.domain.values.users import UserName, Password
from app.infra.dtos.base import TimedBaseModel

if TYPE_CHECKING:
    from app.infra.dtos.packages import Package


class User(TimedBaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[bytes] = mapped_column(String(50))
    packages: Mapped[list['Package']] = relationship(back_populates="owner")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.username!r}"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=UserName(self.username),
            password=Password(self.password),
            created_at=self.created_at
        )
