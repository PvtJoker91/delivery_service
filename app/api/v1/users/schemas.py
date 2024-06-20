from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, ConfigDict

from app.domain.entities.users import User as UserEntity
from app.domain.values.users import UserName, Password


class UserSchema(BaseModel):
    id: int
    username: str

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserSchema':
        return UserSchema(
            id=entity.id,
            username=entity.username.as_generic_type(),
        )


class UserCreateSchema(BaseModel):
    username: str
    password: str

    def to_entity(self):
        return UserEntity(
            username=UserName(self.username),
            password=Password(self.password),
        )
