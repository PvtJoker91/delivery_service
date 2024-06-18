from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, ConfigDict

from app.domain.entities.users import User as UserEntity
from app.domain.values.users import UserName


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserSchema':
        return UserSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
        )


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str

    def to_entity(self):
        return UserEntity(
            first_name=UserName(self.first_name),
            last_name=UserName(self.last_name),
        )
