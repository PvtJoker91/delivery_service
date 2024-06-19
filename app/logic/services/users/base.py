from abc import abstractmethod, ABC
from dataclasses import dataclass

from app.domain.entities.users import User as UserEntity

from app.infra.repositories.users.base import BaseUserRepository


@dataclass
class BaseUserService(ABC):
    repository: BaseUserRepository

    @abstractmethod
    async def create_user(self, user_in: UserEntity) -> UserEntity:
        ...
