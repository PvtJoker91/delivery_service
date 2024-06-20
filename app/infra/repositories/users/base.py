from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.infra.db.users import User


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        ...
