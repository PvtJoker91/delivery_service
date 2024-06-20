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

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserEntity:
        ...

    @abstractmethod
    async def authorise_user(self, username: str, password: str):
        ...
