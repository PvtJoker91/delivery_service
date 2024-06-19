from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.users import User as UserEntity


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity:
        ...
