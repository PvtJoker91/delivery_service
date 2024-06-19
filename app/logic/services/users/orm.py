from abc import  ABC
from dataclasses import dataclass

from app.domain.entities.users import User as UserEntity

from app.infra.repositories.users.base import BaseUserRepository
from app.logic.services.users.base import BaseUserService


@dataclass
class ORMUserService(BaseUserService):
    repository: BaseUserRepository

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        return await self.repository.create_user(user=user_in)
